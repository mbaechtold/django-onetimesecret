import datetime
import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from model_utils import Choices

from onetimesecret import crypto
from onetimesecret.exceptions import PreventModelUpdateException


class Secret(TimeStampedModel):

    LIFETIME_CHOICES = Choices(
        (604800, _("7 days")),
        (259200, _("3 days")),
        (86400, _("1 day")),
        (43200, _("12 hours")),
        (14400, _("4 hours")),
        (3600, _("1 hour")),
        (1800, _("30 minutes")),
        (300, _("5 minutes")),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=8)
    content = models.BinaryField()
    salt = models.BinaryField(null=True, blank=True)
    has_custom_passphrase = models.BooleanField(default=False)
    lifetime = models.IntegerField(choices=LIFETIME_CHOICES, default=0)

    def __str__(self):
        return str(self.pk)

    def get_absolute_url_private(self):
        return reverse("view-secret", kwargs={"key": self.key, "uuid": self.uuid})

    def get_absolute_url_sharing(self):
        return reverse("sharing-instructions", kwargs={"key": self.key, "uuid": self.uuid})

    def save(self, **kwargs):

        if self.pk:
            # Prevent updating of existing instances (because we don't know the password
            # chosen by the user).
            raise PreventModelUpdateException()

        # Encrypt the content before storing the instance in the database.
        passphrase = kwargs.pop("passphrase", None) or settings.SECRET_KEY
        self.salt = crypto.create_salt()
        self.content = crypto.encrypt(self.content, self.salt, passphrase)

        super().save(**kwargs)

    @property
    def expiration_date(self):
        return self.created + datetime.timedelta(0, self.lifetime)
