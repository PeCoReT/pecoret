from rest_framework.test import APITestCase

from attack_surface.models import Target, Service, Finding, Program
from attack_surface.tests.mixin import AttackSurfaceMixin
from pecoret.core.test import PeCoReTTestCaseMixin


class FindingListViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('api:attack_surface:finding-list')
        self.allowed_users = [
            self.pentester2, self.pentester1, self.read_only1
        ]
        self.forbidden_users = [
            self.management1, self.management2, self.customer2, self.customer1, self.user1
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
            self.api_token_check(user, 'scope_attack_surface', self.url, self.client.get, 200, 200, 403)

    def test_api_token_forbidden(self):
        for user in self.forbidden_users:
            self.api_token_check(user, 'scope_attack_surface', self.url, self.client.get, 403, 403, 403)


class FindingCreateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('api:attack_surface:finding-list')
        self.program = self.create_instance(Program)
        self.data = {
            'title': 'SQL Injection on example.com',
            'program': self.program.pk
        }
        self.allowed_users = [
            self.pentester2, self.pentester1, self.read_only1
        ]
        self.forbidden_users = [
            self.management1, self.management2, self.customer2, self.customer1, self.user1
        ]

    def test_allowed(self):
        for user in self.allowed_users:
            finding = self.create_instance(Finding)
            self.data['finding'] = finding.pk
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)

    def test_api_token_allowed(self):
        for user in self.allowed_users:
            finding = self.create_instance(Finding)
            self.data['finding'] = finding.pk
            self.api_token_check(user, 'scope_attack_surface', self.url, self.client.post, 403, 201, 403, data=self.data)

    def test_api_token_forbidden(self):
        for user in self.forbidden_users:
            self.api_token_check(user, 'scope_attack_surface', self.url, self.client.post, 403, 403, 403, data=self.data)


class FindingUpdateViewTestCase(APITestCase, AttackSurfaceMixin):
    def setUp(self):
        self.init_mixin()
        self.finding = self.create_instance(Finding, program=self.program1, locked_by=None)
        self.url = self.get_url('api:attack_surface:finding-detail', pk=self.finding.pk)
        self.allowed_users = [
            self.pentester2, self.pentester1, self.read_only1
        ]
        self.forbidden_users = [
            self.management1, self.management2, self.customer2, self.customer1, self.user1
        ]
        self.data = {
            "name": "NewTitle - 123"
        }

    def test_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)

    def test_locked(self):
        self.finding.locked_by = self.pentester2
        self.finding.save()
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.patch, 400, data=self.data)

    def test_locked_by_self(self):
        self.finding.locked_by = self.pentester1
        self.finding.save()
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)
