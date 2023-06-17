from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models import CWE


class CWEListViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:cwe-list")

    def test_allowed_status(self):
        users = [
            self.pentester1, self.pentester2,
            self.management1, self.management2, self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden_status(self):
        users = [
            self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class CWECreateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:cwe-list")

    def test_not_implemented(self):
        self.client.force_login(self.management2)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 403)


class CWERetrieveViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.entry = self.create_instance(CWE)
        self.url = self.get_url("backend:cwe-detail", pk=self.entry.pk)

    def test_allowed(self):
        users = [
            self.management2, self.management1,
            self.pentester1, self.pentester2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)


class CWEDestroyViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.entry = self.create_instance(CWE)
        self.url = self.get_url("backend:cwe-detail", pk=self.entry.pk)

    def test_not_implemented(self):
        users = [
            self.pentester1, self.pentester2, self.management1, self.management2,
            self.user1, self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)
