from rest_framework.test import APITestCase

from attack_surface.models import Scanner
from pecoret.core.test import PeCoReTTestCaseMixin


class TagListViewSet(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url("api:attack_surface:tag-list")
        self.users_allowed = [
            self.pentester2, self.pentester1, self.read_only1
        ]
        self.users_forbidden = [
            self.customer1, self.customer2,
            self.management2, self.management1, self.user1]

    def test_allowed(self):
        for user in self.users_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_api_token_allowed(self):
        for user in self.users_allowed:
            self.api_token_check(user, 'scope_attack_surface', self.url, self.client.get, 200, 200, 403)

    def test_api_token_forbidden(self):
        for user in self.users_forbidden:
            self.api_token_check(user, 'scope_attack_surface', self.url, self.client.get, 403, 403, 403)


class TagCreateViewSet(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url("api:attack_surface:tag-list")
        self.data = {
            'name': 'testtag',
            'description': 'lorem',
            'color': '#cbcbcb'
        }
        self.allowed_users = [
            self.pentester2, self.pentester1, self.read_only1
        ]
        self.forbidden_users = [
            self.user1, self.customer1, self.customer2,
            self.management1, self.management2
        ]

    def test_allowed(self):
        for user in self.allowed_users:
            self.data['name'] = self.data['name'] + user.username
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)

    def test_api_token_allowed(self):
        for user in self.allowed_users:
            self.data['name'] = self.data['name'] + user.username
            self.api_token_check(user, 'scope_attack_surface', self.url, self.client.post, 403, 201, 403,
                                 data=self.data)

    def test_api_token_forbidden(self):
        for user in self.forbidden_users:
            self.api_token_check(user, 'scope_attack_surface', self.url, self.client.post, 403, 403, 403,
                                 data=self.data)


class TagUpdateCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url("api:attack_surface:tag-create-or-update")
        self.data = {
            'name': 'testtag',
        }

    def test_unique(self):
        self.scanner = self.create_instance(Scanner)
        headers = {'X-Scanner-Auth': self.scanner.token}
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data, headers=headers)
        self.basic_status_code_check(self.url, self.client.post, 200, data=self.data, headers=headers)
