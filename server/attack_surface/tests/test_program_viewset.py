from rest_framework.test import APITestCase

from pecoret.core.test import PeCoReTTestCaseMixin


class TestProgramListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url('api:attack_surface:program-list')

    def test_allowed(self):
        users = [
            self.pentester2, self.pentester1, self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [
            self.management2, self.management1, self.customer1, self.customer2, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_api_token_allowed(self):
        users = [
            self.pentester2, self.pentester1, self.read_only1
        ]
        for user in users:
            self.api_token_check(user, 'scope_attack_surface', self.url, self.client.get, 200, 200, 403)

    def test_api_token_forbidden(self):
        users = [
            self.management2, self.management1, self.customer1, self.customer2, self.user1
        ]
        for user in users:
            self.api_token_check(user, 'scope_attack_surface', self.url, self.client.get, 403, 403, 403)


class ProgramCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url('api:attack_surface:program-list')
        self.data = {
            'name': 'Test Program'
        }
        self.allowed_users = [
            self.pentester2, self.pentester1, self.read_only1
        ]
        self.forbidden_users = [self.management2, self.management1, self.customer1, self.customer2, self.user1]

    def test_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.data['name'] = self.data['name'] + user.username
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
