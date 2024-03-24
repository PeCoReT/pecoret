from rest_framework.test import APITestCase

from pecoret.core.test import PeCoReTTestCaseMixin


class TagListViewSet(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url("asmonitor:tag-list")

    def test_allowed(self):
        users = [
            self.pentester2, self.pentester1, self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [
            self.vendor2, self.vendor1, self.customer1, self.customer2,
            self.management2, self.management1, self.advisory_manager1,
            self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class TagCreateViewSet(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url("asmonitor:tag-list")
        self.data = {
            'name': 'testtag',
            'description': 'lorem',
            'color': '#cbcbcb'
        }
        self.allowed_users = [
            self.pentester2, self.pentester1, self.read_only1
        ]
        self.forbidden_users = [
            self.user1, self.advisory_manager1, self.customer1, self.customer2,
            self.management1, self.management2, self.vendor1, self.vendor2
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
            self.basic_status_code_check(self.url, self.client.get, 403)
            self.set_token_header(token_r)
            self.basic_status_code_check(self.url, self.client.get, 403)
            self.set_token_header(token_w)
            self.basic_status_code_check(self.url, self.client.get, 403)
