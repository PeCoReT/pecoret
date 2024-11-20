from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin


class ShareTokenListViewTestCase(PeCoReTTestCaseMixin, APITestCase):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('api:advisories:share-token-list', advisory=self.advisory1.pk)
        self.users_allowed = [
            self.pentester1, self.read_only1, self.pentester2
        ]
        self.users_forbidden = [self.customer2, self.customer1, self.user1,
            self.management2, self.management1
        ]

    def test_allowed(self):
        for user in self.users_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class ShareTokenCreateViewTestCase(PeCoReTTestCaseMixin, APITestCase):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('api:advisories:share-token-list', advisory=self.advisory1.pk)
        self.users_allowed = [
            self.pentester1, self.read_only1, self.pentester2
        ]
        self.users_forbidden = [self.customer2, self.customer1, self.user1, self.management2, self.management1]

    def test_allowed(self):
        for user in self.users_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)
