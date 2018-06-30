from django_webtest import WebTest


class SharingInstructionsTest(WebTest):
    def test_secret_is_destroyed_after_viewing(self):

        # Alice visits the root of our application.
        response = self.app.get("/")
        assert response.status == "200 OK"

        # Alice creates a secret.
        form = response.form
        form["content"] = "A secret message for Bob from Alice"
        response = form.submit().follow()
        assert response.status == "200 OK"

        # Alice refreshes the sharing instructions but the link to the secret is no longer shown.
        response = self.app.get(response.request.url)
        secret_url = response.html.select("#url-to-secret")[0].attrs["value"]
        assert secret_url == "* * * * * * * * * * * * * * * * * * * * * * * * * * *"
