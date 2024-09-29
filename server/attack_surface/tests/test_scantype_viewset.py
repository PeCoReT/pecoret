from rest_framework.test import APITestCase

from pecoret.core.test import PeCoReTTestCaseMixin


class ScanTypeCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('attack_surface:scan-type-list')
        self.data = {'name': 'Test Port Scan', 'allowed_object_type': 'host', 'conditions': '', 'description': ''}
        self.allowed_users = [self.superuser]
        self.forbidden_users = [self.vendor2, self.vendor1, self.user1, self.customer1, self.customer2,
                                self.management1, self.management2, self.pentester1, self.pentester2]

    def test_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.data['name'] = user.username
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, self.data)


class ScanTypeListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('attack_surface:scan-type-list')
        self.allowed_users = [self.superuser, self.pentester1, self.pentester2, self.read_only1]
        self.forbidden_users = [self.vendor2, self.vendor1, self.user1, self.customer1, self.customer2,
                                self.management1, self.management2]

    def test_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)
