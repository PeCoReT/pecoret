from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin


class GroupListViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:group-list")

    def test_status_forbidden(self):
        users = [self.pentester2, self.pentester1, self.user1, self.read_only1, self.management2, self.management1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_status_allowed(self):
        for user in [self.superuser]:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)


class GroupRetrieveTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.group = Group.objects.get(name="Management")
        self.url = self.get_url("api:backend:group-detail", pk=self.group.pk)

    def test_status_forbidden(self):
        users = [self.pentester2, self.pentester1, self.user1, self.read_only1, self.management2, self.management1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_status_allowed(self):
        for user in [self.superuser]:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)


class GroupDestroyTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.group = Group.objects.get(name="Management")
        self.url = self.get_url("api:backend:group-detail", pk=self.group.pk)

    def test_status_not_implemented(self):
        self.client.force_login(self.superuser)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 405)


class GroupCreateTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:group-list")

    def test_status_not_implemented(self):
        self.client.force_login(self.superuser)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 405)
