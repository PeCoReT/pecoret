from rest_framework.test import APITestCase

from asmonitor.models import Finding, Program, Target
from asmonitor.models.finding import Severity
from pecoret.core.test import PeCoReTTestCaseMixin


class FindingListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.program = self.create_instance(Program)
        self.target = self.create_instance(Target, program=self.program)
        self.url = self.get_url('asmonitor:programs:finding-list', program=self.program.pk)
        self.api_scope = 'scope_asmonitor'
        self.allowed_users = [
            self.pentester2, self.pentester1, self.read_only1
        ]
        self.forbidden_users = [
            self.management1, self.management2, self.customer2, self.customer1,
            self.vendor2, self.vendor1, self.advisory_manager1, self.user1
        ]

    def test_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_api_token_allowed(self):
        for user in self.allowed_users:
            self.api_token_check(user, self.api_scope, self.url, self.client.get, 200, 200, 403)

    def test_api_token_forbidden(self):
        for user in self.forbidden_users:
            self.api_token_check(user, 'scope_asmonitor', self.url, self.client.get, 403, 403, 403)


class FindingCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.program = self.create_instance(Program)
        self.target = self.create_instance(Target, program=self.program)
        self.url = self.get_url('asmonitor:programs:finding-list', program=self.program.pk)
        self.allowed_users = [
            self.pentester1, self.pentester2, self.read_only1
        ]
        self.forbidden_users = [
            self.customer2, self.customer1, self.vendor1, self.vendor2, self.read_only_vendor,
            self.advisory_manager1, self.user1, self.management2, self.management1
        ]
        self.data = {
            'name': 'SQL-Injection', 'proof_text': 'test', 'target': self.target.pk,
            'program': self.program.pk, 'severity': Severity.CRITICAL.label
        }

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
            self.api_token_check(user, 'scope_asmonitor', self.url, self.client.post, 403,
                                 201, 403, data=self.data)

    def test_api_token_forbidden(self):
        for user in self.forbidden_users:
            self.data['name'] = self.data['name'] + user.username
            self.api_token_check(user, 'scope_asmonitor', self.url, self.client.post, 403,
                                 403, 403, data=self.data)


class FindingUpdateView(APITestCase, PeCoReTTestCaseMixin):
    pass


class FindingDestroyView(APITestCase, PeCoReTTestCaseMixin):
    pass


class GlobalFindingListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('asmonitor:finding-list')
        self.program = self.create_instance(Program)
        self.target = self.create_instance(Target, program=self.program)
        self.finding = self.create_instance(Finding, program=self.program, target=self.target)
        self.scope = 'scope_asmonitor'
        self.allowed_users = [
            self.pentester1, self.pentester2, self.read_only1
        ]
        self.forbidden_users = [
            self.customer2, self.customer1, self.vendor2, self.vendor1, self.read_only_vendor,
            self.advisory_manager1, self.management2, self.management1, self.user1
        ]

    def test_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            response = self.basic_status_code_check(self.url, self.client.get, 200)
            self.assertEqual(response.json()['count'], 1)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_api_allowed(self):
        for user in self.allowed_users:
            self.api_token_check(user, self.scope, self.url, self.client.get, 200, 200, 403)

    def test_api_forbidden(self):
        for user in self.forbidden_users:
            self.api_token_check(user, self.scope, self.url, self.client.get, 403, 403, 403)
