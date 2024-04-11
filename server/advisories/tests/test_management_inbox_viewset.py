from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin


class AdvisoryInboxListViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("advisories:inbox-list")
        self.users_forbidden = [
            self.pentester1,
            self.pentester2,
            self.user1,
            self.read_only1,
            self.management1,
            self.management2,
            self.vendor1,
            self.vendor2,
            self.read_only_vendor
        ]

    def test_allowed(self):
        self.client.force_login(self.advisory_manager1)
        response = self.basic_status_code_check(self.url, self.client.get, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["pk"], self.advisory1.pk)

    def test_forbidden(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_api_token_forbidden(self):
        for user in self.users_forbidden:
            self.api_token_check(user, 'scope_advisories', self.url, self.client.get, 403, 403, 403)
