from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models.assets.base import Environment, AssetAccessibility
from backend.models.assets.host import Host


class HostCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:host-list", project=self.project1.pk)
        self.data = {"ip": "10.10.10.10", "dns": "intern.test.,com", "environment": Environment.UNKNOWN.label,
                     "accessible": AssetAccessibility.UNKNOWN.label}
        self.users_allowed = [
            self.pentester1, self.management1
        ]
        self.users_forbidden = [
            self.read_only1, self.management2, self.pentester2, self.user1
        ]

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_api_token_allowed(self):
        for user in self.users_allowed:
            old_ip = int(self.data['ip'].split('.')[-1])
            self.data['ip'] = '.'.join(self.data['ip'].split('.')[:-1]) + f'.{old_ip + 1}'
            self.api_token_check(user, 'scope_all_projects', self.url, self.client.post, 403, 201, 403, data=self.data)

    def test_api_token_forbidden(self):
        for user in self.users_forbidden:
            self.api_token_check(user, 'scope_all_projects', self.url, self.client.post, 403, 403, 403, data=self.data)

    def test_forbidden(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)


class HostUpdateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()


class HostDestroyView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.host1 = self.create_instance(Host, project=self.project1)
        self.host2 = self.create_instance(Host, project=self.project2)
        self.url = self.get_url("api:backend:host-detail", project=self.project1.pk, pk=self.host1.pk)

    def test_forbidden(self):
        users = [
            self.pentester2, self.read_only1, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_broken_access(self):
        url = self.get_url("api:backend:host-detail", project=self.project1.pk, pk=self.host2.pk)
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(url, self.client.delete, 404)


class HostListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.host1 = self.create_instance(Host, project=self.project1)
        self.host2 = self.create_instance(Host, project=self.project2)
        self.url = self.get_url("api:backend:host-list", project=self.project1.pk)

    def test_allowed(self):
        users = [
            self.pentester1, self.management1, self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            response = self.basic_status_code_check(self.url, self.client.get, 200)
            self.assertEqual(response.json()["count"], 1)

    def test_forbidden(self):
        users = [
            self.pentester2, self.user1, self.management2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)
