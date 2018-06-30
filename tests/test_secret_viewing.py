from datetime import datetime

import pytest
import pytz
from django_webtest import WebTest
from freezegun import freeze_time

from onetimesecret.models import Secret
from tests.factories import SecretFactory


class SecretViewingTest(WebTest):
    def test_secret_is_destroyed_after_viewing(self):

        secret = SecretFactory(content="A secret message for Bob from Alice")

        # Bob opens the link he got from Alice.
        response = self.app.get(secret.get_absolute_url_private())
        assert response.status == "200 OK"

        # Bob clicks the confirmation button.
        response = response.form.submit()
        assert response.request.method == "POST"

        # Bob can read the secret.
        the_secret = response.html.select("#the-secret")[0].text
        assert the_secret == "A secret message for Bob from Alice"

        # The secret has been deleted from the database.
        with pytest.raises(Secret.DoesNotExist):
            secret.refresh_from_db()

    def test_repeated_view_of_the_secret_renders_hint(self):
        secret = SecretFactory(content="A secret message for Bob from Alice")

        # Bob opens the link he got from Alice.
        response = self.app.get(secret.get_absolute_url_private())
        assert response.status == "200 OK"

        # Bob clicks the confirmation button.
        response = response.form.submit()
        assert response.request.method == "POST"

        # Bob can read the secret.
        the_secret = response.html.select("#the-secret")[0].text
        assert the_secret == "A secret message for Bob from Alice"

        # Bob tries to access the secret a second time.
        response = self.app.get(secret.get_absolute_url_private())
        assert response.status == "200 OK"
        assert response.html.h1.text == "Unknown Secret"
        assert (
            response.html.find_all("div", class_="alert-warning")[0].text.strip()
            == "The secret message you want to read either never existed or has already been read."
        )

    def test_secret_view_when_secret_no_longer_exists(self):
        secret = SecretFactory(content="A secret message for Bob from Alice")

        # Bob opens the link he fot from Alice.
        response = self.app.get(secret.get_absolute_url_private())
        assert response.status == "200 OK"

        # The secret is deleted in the meantime, maybe because Mallory viewed the secret ;-)
        secret.delete()

        # Bob clicks the confirmation button.
        response = response.form.submit()
        assert response.request.method == "POST"

        # Bob is told that the secret does not exist.
        assert response.html.h1.text == "Unknown Secret"
        assert (
            response.html.find_all("div", class_="alert-warning")[0].text.strip()
            == "The secret message you want to read either never existed or has already been read."
        )

    def test_viewing_secret_with_wrong_password(self):

        # Alice visits the root of our application.
        response = self.app.get("/")
        assert response.status == "200 OK"

        # Alice creates a secret encrypted with a custom passphrase.
        form = response.form
        form["content"] = "A secret message for Bob from Alice"
        form["passphrase"] = "not-for-mallory"
        response = form.submit().follow()
        assert response.status == "200 OK"

        # Alice copies the url to the secret and sends it to Bob.
        secret_url = response.html.select("#url-to-secret")[0].attrs["value"]

        # Bob opens the link he got from Alice.
        response = self.app.get(secret_url)
        assert response.status == "200 OK"

        # Bob enters a wrong passphrase and clicks the confirmation button.
        form = response.form
        form["passphrase"] = "the-wrong-passphrase"
        response = form.submit()
        assert (
            response.html.find_all("div", class_="invalid-feedback")[0].text.strip()
            == "The password is incorrect."
        )

    def test_viewing_an_expired_secret(self):

        date_of_creation = datetime(2015, 1, 1, 14, 0, 0, tzinfo=pytz.UTC)
        date_of_viewing = datetime(2015, 1, 31, 14, 0, 0, tzinfo=pytz.UTC)

        with freeze_time(date_of_creation) as frozen_datetime:
            # Alice creates a secret.
            secret = SecretFactory(content="A secret message for Bob from Alice")

            # Bob waits a few days before viewing the secret.
            frozen_datetime.move_to(date_of_viewing)

            # Bob opens the link he got from Alice.
            response = self.app.get(secret.get_absolute_url_private())
            assert response.status == "200 OK"

            # Bob is told that the secret does not exist.
            assert response.html.h1.text == "Unknown Secret"
            assert (
                response.html.find_all("div", class_="alert-warning")[0].text.strip()
                == "The secret message you want to read either never existed or has already been read."
            )
