from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import FormView
from django.views.generic import TemplateView

from onetimesecret import crypto
from onetimesecret.forms import CreateSecretForm
from onetimesecret.forms import ViewSecretConfirmationForm
from onetimesecret.models import Secret
from onetimesecret.utils import create_secret


class CreateSecret(FormView):

    template_name = "onetimesecret/create_secret.html"
    form_class = CreateSecretForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):

        custom_passphrase = form.cleaned_data["passphrase"]

        secret = create_secret(
            content=form.cleaned_data["content"],
            passphrase=custom_passphrase,
            has_custom_passphrase=bool(custom_passphrase),
            lifetime=form.cleaned_data["lifetime"],
        )

        # The sharing instructions shown to Alice are secrets too. The content
        # of this secret is the primary key of the secret Alice wants to send to Bob.
        self.sharing_instruction = create_secret(str(secret.pk))

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(
            "sharing-instructions",
            kwargs={"key": self.sharing_instruction.key, "uuid": self.sharing_instruction.uuid},
        )


class ShowSharingInstructions(TemplateView):

    template_name = "onetimesecret/sharing_instructions.html"

    def get(self, request, *args, **kwargs):
        key = kwargs.pop("key")
        uuid = kwargs.pop("uuid")

        try:
            self.sharing_instruction = Secret.objects.get(key=key, uuid=uuid)
        except Secret.DoesNotExist:
            self.sharing_instruction = None

        if self.sharing_instruction:
            self.sharing_instruction.delete()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["secret"] = {}

        if self.sharing_instruction:
            secret_pk = int(
                crypto.decrypt(
                    self.sharing_instruction.content,
                    self.sharing_instruction.salt,
                    passphrase=settings.SECRET_KEY,
                )
            )
            secret = Secret.objects.get(pk=secret_pk)

            context["secret"].update(
                {
                    "lifetime_display": secret.get_lifetime_display(),
                    "expiration_date": secret.expiration_date,
                    "url": self.request.build_absolute_uri(secret.get_absolute_url_private()),
                }
            )

        return context


class ViewSecret(FormView):

    form_class = ViewSecretConfirmationForm

    def dispatch(self, request, *args, **kwargs):
        self.secret = self.get_secret()
        return super(ViewSecret, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.render_to_response(
            self.get_context_data(), "onetimesecret/view_secret_confirmation.html"
        )

    def post(self, request, *args, **kwargs):
        if not self.secret:
            return self.get(request, *args, **kwargs)

        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["secret"] = self.secret
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        context["plaintext"] = crypto.decrypt(
            self.secret.content,
            self.secret.salt,
            passphrase=form.cleaned_data.get("passphrase", settings.SECRET_KEY),
        )
        self.secret.delete()
        return self.render_to_response(context, "onetimesecret/view_secret.html")

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form), "onetimesecret/view_secret_confirmation.html"
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["secret_exists"] = bool(self.secret)
        return context_data

    def get_secret(self):
        key = self.kwargs.get("key", "")
        uuid = self.kwargs.get("uuid", "")

        try:
            secret = Secret.objects.get(key=key, uuid=uuid)
        except Secret.DoesNotExist:
            secret = None

        if secret and now() > secret.expiration_date:
            secret = None

        return secret

    def render_to_response(self, context, template, **response_kwargs):
        response_kwargs.setdefault("content_type", self.content_type)
        return self.response_class(
            request=self.request,
            template=template,
            context=context,
            using=self.template_engine,
            **response_kwargs
        )
