from uuid import uuid4

import pytest
from django.test import TestCase

from onetimesecret.exceptions import PreventModelUpdateException
from onetimesecret.models import Secret
from tests.factories import SecretFactory


class TestSecretModel(TestCase):
    def test_create_valid_secret_instance(self):

        secret = Secret(key="abcdefg", content="Hello World", lifetime=604800)
        secret.save()
        secret.full_clean()

    def test_secret_factory(self):

        secret = SecretFactory()
        secret.full_clean()

    def test_string_representation(self):

        secret = SecretFactory()
        assert str(secret) == "1"

    def test_updating_secret_is_prohibited(self):

        secret = SecretFactory()
        secret.key = "somekey"

        with pytest.raises(PreventModelUpdateException):
            secret.save()

    def test_get_absolute_url_private(self):

        uuid = uuid4()
        secret = SecretFactory(uuid=uuid, key="somekey")
        assert secret.get_absolute_url_private() == f"/secret/somekey/{uuid}/"

    def test_get_absolute_url_sharing(self):

        uuid = uuid4()
        secret = SecretFactory(uuid=uuid, key="somekey")

        assert secret.get_absolute_url_sharing() == f"/private/somekey/{uuid}/"
