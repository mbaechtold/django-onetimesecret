from cryptography.fernet import InvalidToken
from django import forms
from django.utils.translation import gettext_lazy as _

from onetimesecret import crypto
from onetimesecret.models import Secret


class CreateSecretForm(forms.Form):

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": _("Enter the secret information you want to share with somebody...")
            }
        ),
        required=True,
    )
    passphrase = forms.CharField(
        label=_("Password (optional)"),
        help_text=_(
            "The viewer needs to enter this password in order to view the secret. You "
            "need to tell it to the receiver yourself."
        ),
        required=False,
        widget=forms.TextInput(attrs={"placeholder": ""}),
    )
    lifetime = forms.ChoiceField(
        label=_("Lifetime"),
        help_text=_(
            "The secret will be deleted after its lifetime has exceeded, even if it has not been viewed."
        ),
        required=True,
        choices=Secret.LIFETIME_CHOICES,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial["lifetime"] = 604800


class ViewSecretConfirmationForm(forms.Form):

    passphrase = forms.CharField(
        label=_("Password"),
        help_text=_(
            "The creator of the secret used a custom password to encrypt the secret. Please enter it here."
        ),
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": ""}),
    )

    def __init__(self, secret=None, *args, **kwargs):
        self.secret = secret

        super().__init__(*args, **kwargs)

        if not self.secret or not self.secret.has_custom_passphrase:
            self.fields.pop("passphrase")

    def clean(self):
        super().clean()
        self.validate_passphrase()

    def validate_passphrase(self):
        """
        Validate the passphrase by attempting to decrypt the encrypted secret.
        """
        if "passphrase" in self.cleaned_data:
            try:
                crypto.decrypt(
                    self.secret.content,
                    self.secret.salt,
                    passphrase=self.cleaned_data["passphrase"],
                )
            except InvalidToken:
                msg = _("The password is incorrect.")
                self.add_error("passphrase", msg)
