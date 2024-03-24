from rest_framework.test import APITestCase

from asmonitor.models import Target, Program
from pecoret.core.test import PeCoReTTestCaseMixin


class TargetListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.target = self.create_instance(Target)
        self.url = self.get_url('asmonitor:programs:target-list', program=self.target.program.pk)

    def test_allowed(self):
        users = [
            self.pentester1, self.pentester2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)


class TargetCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.program = self.create_instance(Program)
        self.data = {
            'ip': '10.10.10.10',
            'name': 'Test'
        }
        self.url = self.get_url('asmonitor:programs:target-list', program=self.program.pk)
        self.allowed_users = [
            self.pentester1, self.pentester2, self.read_only1
        ]
        self.forbidden_users = [
            self.management1, self.management2, self.customer2, self.customer1, self.vendor1,
            self.vendor2, self.advisory_manager1, self.user1, self.read_only_vendor
        ]

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
            token_w, token_r, token_n = self.create_api_tokens_scope(user, scope='scope_asmonitor')
            self.set_token_header(token_w)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)
            self.set_token_header(token_r)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)
            self.set_token_header(token_n)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)

    def test_api_token_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            token_w, token_r, token_n = self.create_api_tokens_scope(user, scope='scope_asmonitor')
            self.set_token_header(token_n)
            self.basic_status_code_check(self.url, self.client.post, 403)
            self.set_token_header(token_r)
            self.basic_status_code_check(self.url, self.client.post, 403)
            self.set_token_header(token_w)
            self.basic_status_code_check(self.url, self.client.post, 403)


class GlobalTargetViewSet(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.target = self.create_instance(Target)
        self.url = self.get_url('asmonitor:target-list')
        self.allowed_users = [
            self.pentester1, self.pentester2, self.read_only1
        ]
        self.forbidden_users = [
            self.management1, self.management2, self.customer2, self.user1,
            self.vendor1, self.vendor2, self.advisory_manager1, self.customer1,
            self.customer2
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
            token_w, token_r, token_n = self.create_api_tokens_scope(user, scope='scope_asmonitor')
            self.set_token_header(token_w)
            self.basic_status_code_check(self.url, self.client.get, 200)
            self.set_token_header(token_r)
            self.basic_status_code_check(self.url, self.client.get, 200)
            self.set_token_header(token_n)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_api_token_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            token_w, token_r, token_n = self.create_api_tokens_scope(user, scope='scope_asmonitor')
            self.set_token_header(token_n)
            self.basic_status_code_check(self.url, self.client.get, 403)
            self.set_token_header(token_r)
            self.basic_status_code_check(self.url, self.client.get, 403)
            self.set_token_header(token_w)
            self.basic_status_code_check(self.url, self.client.get, 403)
