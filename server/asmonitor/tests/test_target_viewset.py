from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from asmonitor.models import Target, Program


class TargetListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.target = self.create_instance(Target)
        self.url = self.get_url('asmonitor:target-list', program=self.target.program.pk)

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
        self.url = self.get_url('asmonitor:target-list', program=self.program.pk)

    def test_allowed(self):
        users = [
            self.pentester1, self.pentester2, self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            self.data['name'] = self.data['name'] + user.username
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        users = [
            self.management1, self.management2, self.customer2, self.customer1, self.vendor1,
            self.vendor2, self.advisory_manager1, self.user1, self.read_only_vendor
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)
