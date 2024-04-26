from rest_framework.test import APITestCase

from asmonitor.models import TargetMeta, Target
from pecoret.core.test import PeCoReTTestCaseMixin


class TargetMetaListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.targetmeta = self.create_instance(TargetMeta)
        self.url = self.get_url('asmonitor:targets:meta-list', program=self.targetmeta.target.program.pk,
                                target=self.targetmeta.target.pk)
        self.users_forbidden = [
            self.customer2, self.customer1, self.vendor2, self.vendor1,
            self.management2, self.management1, self.advisory_manager1,
            self.user1
        ]
        self.users_allowed = [
            self.read_only1, self.pentester2, self.pentester1
        ]

    def test_allowed(self):
        for user in self.users_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_api_token_allowed(self):
        for user in self.users_allowed:
            self.api_token_check(user, 'scope_asmonitor', self.url, self.client.get, 200, 200, 403)

    def test_api_token_forbidden(self):
        for user in self.users_forbidden:
            self.api_token_check(user, 'scope_asmonitor', self.url, self.client.get, 403, 403, 403)

    def test_forbidden(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class TargetMetaCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.target = self.create_instance(Target)
        self.data = {
            'key': 'urls',
            'value': 'https://example.com\nhttps://example.com/admin'
        }
        self.url = self.get_url('asmonitor:targets:meta-list', program=self.target.program.pk, target=self.target.pk)
        self.allowed_users = [
            self.pentester1, self.pentester2, self.read_only1
        ]
        self.forbidden_users = [
            self.management1, self.management2, self.customer2, self.customer1,
            self.vendor1, self.vendor2, self.read_only_vendor, self.user1,
            self.advisory_manager1
        ]

    def test_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.data['key'] = user.username
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)

    def test_api_token_allowed(self):
        for user in self.allowed_users:
            self.data['key'] = user.username
            self.api_token_check(user, 'scope_asmonitor', self.url, self.client.post, 403, 201, 403, data=self.data)

    def test_api_token_forbidden(self):
        for user in self.forbidden_users:
            self.api_token_check(user, 'scope_asmonitor', self.url, self.client.post, 403, 403, 403, data=self.data)
