from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin


class UserSettingsRetrieveViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url("api:backend:user-settings-detail")

    def test_unauthorized(self):
        self.basic_status_code_check(self.url, self.client.get, 403)

    def test_allowed(self):
        users = [
            self.pentester1,
            self.pentester2,
            self.management1,
            self.management2,
            self.user1,
            self.read_only1,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)


class UserSettingsUpdateTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url("api:backend:user-settings-detail")
        self.data = {"show_real_name_in_report": True}

    def test_unauthorized(self):
        self.basic_status_code_check(self.url, self.client.get, 403)

    def test_allowed(self):
        users = [
            self.pentester1,
            self.pentester2,
            self.management1,
            self.management2,
            self.user1,
            self.read_only1,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.patch, 200, data=self.data
            )
