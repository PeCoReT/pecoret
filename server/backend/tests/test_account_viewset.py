from rest_framework.test import APITestCase

from pecoret.core.test import PeCoReTTestCaseMixin


class AccountListViewSet(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:account-list", project=self.project1.pk)
        self.users_allowed = [
            self.read_only1, self.pentester1, self.management1
        ]
        self.users_forbidden = [
            self.pentester2, self.management2, self.user1, self.customer1, self.customer2,
        ]

    def test_allowed_status(self):
        for user in self.users_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_api_token_allowed(self):
        for user in self.users_allowed:
            self.api_token_check(user, 'scope_all_projects', self.url, self.client.get, 200, 200, 403)

    def test_api_token_forbidden(self):
        for user in self.users_forbidden:
            self.api_token_check(user, 'scope_all_projects', self.url, self.client.get, 403, 403, 403)

    def test_forbidden_status(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class AccountCreateViewSet(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:account-list", project=self.project1.pk)
        self.data = {
            "role": "Admin",
            "username": "TestAdmin",
            "accessible": False,
            "compromised": False,
            "password": "",
            "description": "just a user account."
        }
        self.users_allowed = [
            self.pentester1, self.management1
        ]
        self.users_forbidden = [
            self.read_only1, self.user1, self.pentester2, self.management2, self.customer1, self.customer2, self.user1
        ]

    def test_allowed_status(self):
        for user in self.users_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 201, data=self.data
            )

    def test_api_token_allowed(self):
        for user in self.users_allowed:
            self.api_token_check(user, 'scope_all_projects', self.url, self.client.post, 403, 201, 403, data=self.data)

    def test_api_token_forbidden(self):
        for user in self.users_forbidden:
            self.api_token_check(user, 'scope_all_projects', self.url, self.client.post, 403, 403, 403, data=self.data)

    def test_forbidden_status(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 403, data=self.data
            )


class AccountUpdateViewSet(APITestCase, PeCoReTTestCaseMixin):
    # TODO: implement
    pass


class AccountDeleteViewSet(APITestCase, PeCoReTTestCaseMixin):
    # TODO: implement
    pass
