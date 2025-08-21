from django.core import mail
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models import User
from backend.utils.change_email_token_generator import change_email_token_generator


class ChangeEmailViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:user-change-email")
        self.data = {"password": "changeme", "email": "mynewemail@example.com"}

    def test_valid(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 200, data=self.data)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(User.objects.filter(new_email=self.data['email']).exists(), True)

    def test_invalid_password(self):
        self.client.force_login(self.pentester1)
        self.data["password"] = "invalid"
        self.basic_status_code_check(self.url, self.client.post, 400, data=self.data)
        self.assertEqual(len(mail.outbox), 0)


class ChangeEmailConfirmView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.pentester1.new_email = "asdf@example.com"
        self.pentester2.new_email = "asdf2@example.com"
        self.pentester1.save()
        self.pentester2.save()
        self.uid = force_str(urlsafe_base64_encode(force_bytes(self.pentester1.pk)))
        self.token = change_email_token_generator.make_token(self.pentester1)
        self.url = self.get_url("api:backend:user-change-email-confirm")
        self.data = {"uid": self.uid, "token": self.token}

    def test_valid(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 204, data=self.data)

    def test_invalid_user(self):
        self.client.force_login(self.pentester2)
        self.basic_status_code_check(self.url, self.client.post, 400, data=self.data)

    def test_invalid_token(self):
        uid2 = force_str(urlsafe_base64_encode(force_bytes(self.pentester2.pk)))
        self.data["uid"] = uid2
        self.client.force_login(self.pentester2)
        self.basic_status_code_check(self.url, self.client.post, 400, data=self.data)
