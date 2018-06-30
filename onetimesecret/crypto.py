import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def create_salt():

    return os.urandom(16)


def encrypt(plaintext, salt, passphrase):

    passphrase = passphrase.encode("utf-8")
    plaintext = plaintext.encode("utf-8")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    key = base64.urlsafe_b64encode(kdf.derive(passphrase))

    f = Fernet(key)
    return f.encrypt(plaintext)


def decrypt(ciphertext, salt, passphrase):

    passphrase = passphrase.encode("utf-8")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    key = base64.urlsafe_b64encode(kdf.derive(passphrase))

    f = Fernet(key)
    return f.decrypt(ciphertext).decode("utf-8")
