from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin


class LabelListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:advisories:advisory-label-list")
        self.users_allowed = [self.pentester1, self.pentester2, self.read_only1]
        self.users_forbidden = [
            self.management1, self.management2, self.user1, self.customer1, self.customer2]

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
            self.api_token_check(user, 'scope_advisories', self.url, self.client.get, 200, 200, 403)

    def test_api_token_forbidden(self):
        for user in self.users_forbidden:
            self.api_token_check(user, 'scope_advisories', self.url, self.client.get, 403, 403, 403)


class LabelCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:advisories:advisory-label-list")
        self.data = {"name": "test", "description": "lorem", "color": "#fff"}
        self.allowed_users = [self.pentester1, self.pentester2, self.read_only1]
        self.forbidden_users = [self.user1, self.management1, self.management2, self.customer2, self.customer1
        ]

    def test_allowed(self):
        for user in self.allowed_users:
            self.data['name'] = user.username
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)

    def test_color_validation(self):
        self.data["color"] = '"invalid'
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 400, data=self.data)
