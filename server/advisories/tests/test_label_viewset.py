from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin


class LabelListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("advisories:label-list")

    def test_allowed(self):
        users = [
            self.advisory_manager1,
            self.pentester1, self.pentester2,
            self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [
            self.management1, self.management2,
            self.vendor1, self.vendor2,
            self.read_only_vendor, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class LabelCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("advisories:label-list")
        self.data = {"name": "test", "description": "lorem", "color": "#fff"}

    def test_allowed(self):
        users = [
            self.advisory_manager1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        users = [
            self.pentester1, self.pentester2,
            self.management2, self.management1,
            self.read_only1, self.read_only_vendor,
            self.vendor2, self.vendor1, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)

    def test_color_validation(self):
        self.data["color"] = '"invalid'
        self.client.force_login(self.advisory_manager1)
        self.basic_status_code_check(self.url, self.client.post, 400, data=self.data)
