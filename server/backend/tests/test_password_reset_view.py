from rest_framework.test import APITestCase
from django.contrib.auth.tokens import default_token_generator
from pecoret.core import utils
from pecoret.core.test import PeCoReTTestCaseMixin


class PasswordResetView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:user-reset-password")
        self.data = {"email": self.pentester1.email}

    def test_working(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 204)
        # TODO: fix github action django-q2
        # self.assertEqual(len(mail.outbox), 1)

    def test_invalid(self):
        response = self.client.post(self.url, {"email": "asdasdasd@easdad.com"})
        self.assertEqual(response.status_code, 204)


class PasswordResetConfirmView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.token = default_token_generator.make_token(self.pentester1)
        self.uid = utils.encode_uid(self.pentester1.pk)
        self.url = self.get_url("api:backend:user-reset-password-confirm")
        self.data = {"token": self.token, "uid": self.uid, "new_password": "myCoolTest1234!1234"}

    def test_working(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 204)
        # test login working
        login_url = self.get_url("api:backend:login")
        response = self.client.post(login_url, {"username": self.pentester1.username,
                                                "password": self.data["new_password"]})
        self.assertEqual(response.status_code, 200)
        self.assertIn("csrf_token", response.json())
