from django.contrib.auth.models import Group
from rest_framework.test import APITestCase

from backend.models import User
from pecoret.core.test import PeCoReTTestCaseMixin


class UserListViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:user-list")

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
        self.url = self.get_url("api:backend:user-detail", pk=self.test_user.pk)

    def test_delete_not_allowed(self):
        self.client.force_login(self.management1)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)


class UserUpdateViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.test_user = self.create_user("test_user123", "changeme1234")
        self.url = self.get_url("api:backend:user-detail", pk=self.test_user.pk)
        self.data = {'is_active': False}

    def test_update_not_allowed(self):
        self.client.force_login(self.management1)
        data = {"username": "admin"}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, 403)

    def test_group_changed(self):
        self.client.force_login(self.superuser)
        data = {"groups": [Group.objects.get(name="Management").pk]}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(User.objects.get(username="test_user123").groups.values_list("pk", flat=True)),
                         data["groups"])

    def test_forbidden(self):
        users = [
            self.management1, self.management2, self.user1, self.pentester1, self.pentester2, self.customer2,
            self.customer1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)


class UserCreateViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:user-list")
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

    def test_superuser_initial_password(self):
        self.client.force_login(self.superuser)
        self.data['password'] = 'test1234!asdf'
        response = self.client.post(self.url, self.data)
        user = User.objects.get(username="tlast")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.filter(username="tlast").count(), 1)
        self.assertEqual(user.has_usable_password(), True)


class ChangePasswordView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.pentester1.set_password('test123')
        self.pentester1.save()
        self.url = self.get_url('headless:browser:account:change_password')
        self.data = {
            'current_password': 'test123',
            'new_password': 'test1234!Changemevvvv!?'
        }

    def test_working(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 200, data=self.data)
        user = User.objects.get(pk=self.pentester1.pk)
        self.assertEqual(user.check_password('test1234!Changemevvvv!?'), True)
        self.assertEqual(user.check_password('test123'), False)

    def test_wrong_old_password(self):
        self.data['current_password'] = 'invalid'
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
        self.url = self.get_url('api:backend:user-update-profile')
        self.data = {'first_name': 'TestUser'}

    def test_allowed(self):
        users = [
            self.management1, self.management2, self.pentester1, self.pentester2,
            self.customer1, self.customer2
        ]
        for user in users:
            self.client.force_login(user)
            response = self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)
            self.assertEqual(response.json()['first_name'], self.data['first_name'])

    def test_forbidden_fields(self):
        users = [
            self.management1, self.management2,
            self.read_only1, self.pentester1, self.pentester2,
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
