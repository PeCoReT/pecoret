from rest_framework.test import APITestCase
from attack_surface.models.program import Program
from attack_surface.models.target import DataTypes, ScopeChoices
from pecoret.core.test import PeCoReTTestCaseMixin


class TargetListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url('api:attack_surface:target-list')
        self.users_forbidden = [
            self.customer2, self.customer1, self.management1, self.management2, self.user1
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


class TargetCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.program = self.create_instance(Program)
        self.data = {
            'data': 'example.com',
            'program': self.program.pk,
            'scope': ScopeChoices.IN_SCOPE.label,
            'data_type': DataTypes.SUBDOMAIN.label
        }
        self.url = self.get_url('api:attack_surface:target-list')
        self.forbidden_users = [
            self.management1, self.management2, self.customer2, self.customer1, self.user1,
            self.pentester1, self.pentester2, self.read_only1

        ]

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)

    def test_api_token_forbidden(self):
        for user in self.forbidden_users:
            self.api_token_check(user, 'scope_attack_surface', self.url, self.client.post, 403, 403, 403,
                                 data=self.data)
