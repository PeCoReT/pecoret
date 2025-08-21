from rest_framework.test import APITestCase

from attack_surface.models import Scanner
from pecoret.core.test import PeCoReTTestCaseMixin


class ScannerCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('api:attack_surface:scanner-list')
        self.data = {
            'name': 'Test Scanner',
        }
        self.allowed_users = [self.superuser]
        self.forbidden_users = [self.user1, self.customer1, self.customer2,
                                self.management1, self.management2]

    def test_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.data['name'] = user.username
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, self.data)


class ScannerListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('api:attack_surface:scanner-list')
        self.allowed_users = [self.superuser, self.pentester1, self.pentester2, self.read_only1]
        self.forbidden_users = [self.user1, self.customer1, self.customer2,
                                self.management1, self.management2]

    def test_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            response = self.basic_status_code_check(self.url, self.client.get, 200)
            # ensure token is not leaked
            self.assertEqual(response.json().get('token'), None)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class ScannerLastSeen(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.scanner = self.create_instance(Scanner)
        self.url = self.get_url('api:attack_surface:scanner-ping')
        self.allowed_users = []
        self.forbidden_users = [self.user1, self.customer1, self.customer2,
                                self.pentester1, self.pentester2, self.read_only1, self.management2, self.management1]

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data={})

    def test_scanner_token(self):
        headers = {'X-Scanner-Auth': self.scanner.token}
        response = self.basic_status_code_check(self.url, self.client.post, 200, data={}, headers=headers)
        self.assertNotEqual(response.json().get('last_seen'), None)

    def test_invalid_scanner_token(self):
        scanner = self.create_instance(Scanner)
        headers = {'X-Scanner-Auth': scanner.token + "-invalid"}
        self.basic_status_code_check(self.url, self.client.post, 403, data={}, headers=headers)
