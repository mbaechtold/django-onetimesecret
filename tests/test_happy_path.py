from django_webtest import WebTest


class HappyPathTest(WebTest):
    def test_happy_path_without_custom_passphrase(self):
        """
        Test the happy path from the start to the end where Bob creates a secret
        and Alice retrieves the secret.

        """
        # Alice visits the root of our application.
        response = self.app.get("/")
        assert response.status == "200 OK"

        # Alice creates a secret.
        form = response.form
        form["content"] = "A secret message for Bob"
        response = form.submit().follow()
        assert response.status == "200 OK"

        # Alice copies the url to the secret and sends it to Bob.
        secret_url = response.html.select("#url-to-secret")[0].attrs["value"]

        # Bob opens the link he got from Alice.
        response = self.app.get(secret_url)
        assert response.status == "200 OK"

        # Bob clicks the confirmation button.
        response = response.form.submit()

        # Bob can read the secret.
        the_secret = response.html.select("#the-secret")[0].text
        assert the_secret == "A secret message for Bob"

    def test_happy_path_with_custom_passphrase(self):
        """
        Test the happy path from the start to the end where Bob creates a secret,
        encrypted with a custom passphrase, and Alice retrieves the secret.

        """
        # Alice visits the root of our application.
        response = self.app.get("/")
        assert response.status == "200 OK"

        # Alice creates a secret encrypted with a custom passphrase.
        form = response.form
        form["content"] = "A secret message for Bob"
        form["passphrase"] = "not-for-mallory"
        response = form.submit().follow()
        assert response.status == "200 OK"

        # Alice copies the url to the secret and sends it to Bob.
        secret_url = response.html.select("#url-to-secret")[0].attrs["value"]

        # Bob opens the link he got from Alice.
        response = self.app.get(secret_url)
        assert response.status == "200 OK"

        # Bob enters the passphrase and clicks the confirmation button.
        form = response.form
        form["passphrase"] = "not-for-mallory"
        response = form.submit()

        # Bob can read the secret.
        the_secret = response.html.select("#the-secret")[0].text
        assert the_secret == "A secret message for Bob"
