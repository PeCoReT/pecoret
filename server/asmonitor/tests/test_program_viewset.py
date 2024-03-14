from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin


class TestProgramListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url('asmonitor:program-list')

    def test_allowed(self):
        users = [
            self.pentester2, self.pentester1, self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [
            self.management2, self.management1, self.advisory_manager1, self.read_only_vendor,
            self.vendor2, self.vendor1, self.customer1, self.customer2, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class ProgramCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url('asmonitor:program-list')
        self.data = {
            'name': 'Test Program'
        }

    def test_allowed(self):
        users = [
            self.pentester2, self.pentester1, self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            self.data['name'] = self.data['name'] + user.username
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        users = [
            self.management2, self.management1, self.read_only_vendor, self.vendor2, self.vendor1,
            self.advisory_manager1, self.customer1, self.customer2, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)
