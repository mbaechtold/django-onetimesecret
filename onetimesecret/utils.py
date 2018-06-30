import random

from onetimesecret.models import Secret


def create_secret(content, passphrase=None, **kwargs):

    secret = Secret(
        key="".join(random.choice("23456789abcdefghjkmnpqrstuvwx") for _ in range(8)),
        content=content,
        **kwargs,
    )
    secret.save(passphrase=passphrase)

    return secret
