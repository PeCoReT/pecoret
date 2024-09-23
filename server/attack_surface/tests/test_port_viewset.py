from rest_framework.test import APITestCase

from attack_surface.models import Program, Host
from attack_surface.models.port import Protocol
from pecoret.core.test import PeCoReTTestCaseMixin


class PortListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('attack_surface:port-list')
        self.users_forbidden = [
            self.customer2, self.customer1, self.management2, self.management1, self.vendor1, self.vendor2,
            self.user1
        ]
        self.users_allowed = [
            self.read_only1, self.pentester2, self.pentester1
        ]

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


class PortCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.program = self.create_instance(Program)
        self.host = self.create_instance(Host, ip_address='10.10.10.10')
        self.data = {
            'number': 80, 'service_name': 'http',
            'banner': 'test', 'protocol': Protocol.TCP.label, 'host': self.host.pk
        }
        self.url = self.get_url('attack_surface:port-list')
        self.allowed_users = [
            self.pentester1, self.pentester2, self.read_only1
        ]
        self.forbidden_users = [
            self.management1, self.management2, self.customer2, self.customer1, self.vendor1,
            self.vendor2, self.user1
        ]

    def test_allowed(self):
        for user in self.allowed_users:
            self.data['number'] += 1
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)

    def test_api_token_allowed(self):
        for user in self.allowed_users:
            self.data['number'] += 1
            self.api_token_check(user, 'scope_attack_surface', self.url, self.client.post, 403, 201, 403,
                                 data=self.data)

    def test_api_token_forbidden(self):
        for user in self.forbidden_users:
            self.api_token_check(user, 'scope_attack_surface', self.url, self.client.post, 403, 403, 403,
                                 data=self.data)
