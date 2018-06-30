import factory

from onetimesecret import models


class SecretFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Secret

    key = "abc1234"
    content = "Hello World"
    lifetime = 604800
