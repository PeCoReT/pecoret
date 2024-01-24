from django.contrib.auth.models import Group, PermissionsMixin
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core import mail
from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models import User


class UserListViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:user-list")

    def test_allowed_status(self):
        for user in [self.management1]:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden_status(self):
        for user in [self.user1, self.pentester1, self.pentester2, self.read_only1]:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class UserDeleteViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.test_user = self.create_user("test_user123", "changeme1234")
        self.url = self.get_url("backend:user-detail", pk=self.test_user.pk)

    def test_delete_not_allowed(self):
        self.client.force_login(self.management1)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)


class UserUpdateViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.test_user = self.create_user("test_user123", "changeme1234")
        self.url = self.get_url("backend:user-detail", pk=self.test_user.pk)
        self.data = {'is_active': False}

    def test_update_not_allowed(self):
        self.client.force_login(self.management1)
        data = {"username": "admin"}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, 403)

    def test_group_changed(self):
        self.client.force_login(self.superuser)
        data = {"groups": [Group.objects.get(name="Advisory Management").pk]}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(User.objects.get(username="test_user123").groups.values_list("pk", flat=True)),
                         data["groups"])

    def test_forbidden(self):
        users = [
            self.management1, self.management2, self.advisory_manager1, self.vendor1,
            self.vendor2, self.user1, self.pentester1,self.pentester2, self.customer2,
            self.customer1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)


class UserCreateViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:user-list")
        self.data = {"first_name": "Test", "last_name": "Last", "username": "tlast", "email": "test@eexample.ccom",
                     "groups": [Group.objects.get(name="Pentester").pk]}

    def test_create_forbidden(self):
        self.client.force_login(self.management1)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 403)

    def test_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.filter(username="tlast").count(), 1)
        user = User.objects.get(username="tlast")
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.has_usable_password(), False)
        self.assertEqual(len(mail.outbox), 1)


class AccountActivationView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.activation_user = self.create_user("testactivation", None, is_active=False)
        self.uid = force_str(urlsafe_base64_encode(force_bytes(self.activation_user.pk)))
        self.token = default_token_generator.make_token(self.activation_user)
        self.url = self.get_url("backend:user-activation")
        self.data = {"uid": self.uid, "token": self.token, "new_password": "mysupersecurepassword1234!"}

    def test_activation(self):
        self.assertEqual(self.activation_user.has_usable_password(), False)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 204)
        user = User.objects.get(username="testactivation")
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.has_usable_password(), True)

        # test login
        login_url = self.get_url("backend:login")
        data = {"username": "testactivation", "password": "mysupersecurepassword1234!"}
        response = self.client.post(login_url, data)
        self.assertIn("csrf_token", response.json())
        self.assertEqual(response.json().get("user", {}).get("username"), "testactivation")

    def test_invalid_token(self):
        # TODO: fixme
        headers = {"X-CSRFToken": "random"}
        response = self.client.post(self.url, self.data, headers=headers)
        # self.assertEqual(response.status_code, 400)


class ChangePasswordView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.pentester1.set_password('test123')
        self.pentester1.save()
        self.url = self.get_url('backend:user-change-password')
        self.data = {
            'old_password': 'test123',
            'new_password': 'test1234!Changemevvvv!?'
        }

    def test_working(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 200, data=self.data)
        user = User.objects.get(pk=self.pentester1.pk)
        self.assertEqual(user.check_password('test1234!Changemevvvv!?'), True)
        self.assertEqual(user.check_password('test123'), False)

    def test_wrong_old_password(self):
        self.data['old_password'] = 'invalid'
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 400, data=self.data)
        user = User.objects.get(pk=self.pentester1.pk)
        self.assertEqual(user.check_password('test1234!Changemevvvv!?'), False)
        self.assertEqual(user.check_password('test123'), True)

    def test_validate_new_password(self):
        self.data['new_password'] = 'test'
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 400, data=self.data)
        user = User.objects.get(pk=self.pentester1.pk)
        self.assertEqual(user.check_password('test1234!Changemevvvv!?'), False)
        self.assertEqual(user.check_password('test123'), True)


class UserProfileUpdateViewTest(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url('backend:user-update-profile')
        self.data = {'first_name': 'TestUser'}

    def test_allowed(self):
        users = [
            self.management1, self.management2, self.vendor1, self.vendor2, self.read_only_vendor,
            self.read_only_vendor, self.pentester1, self.pentester2, self.advisory_manager1,
            self.customer1, self.customer2
        ]
        for user in users:
            self.client.force_login(user)
            response = self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)
            self.assertEqual(response.json()['first_name'], self.data['first_name'])

    def test_forbidden_fields(self):
        users = [
            self.management1, self.management2, self.vendor1, self.vendor2, self.read_only_vendor,
            self.read_only1, self.read_only_vendor, self.pentester1, self.pentester2, self.advisory_manager1,
            self.customer2, self.customer1
        ]
        self.data['email'] = 'e@example.test'
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)
            new_user = User.objects.get(pk=user.pk)
            self.assertEqual(new_user.email, user.email)

    def test_customer_cannot_change_company(self):
        self.data['company'] = self.customer1.company.pk
        self.client.force_login(self.customer1)
        self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)
        new_customer = User.objects.get(pk=self.customer1.pk)
        self.assertEqual(self.customer1.company.pk, new_customer.company.pk)
