from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models import Technology


class TechnologyListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.tech1 = self.create_instance(Technology)
        self.url = self.get_url('api:backend:technology-list')

    def test_allowed(self):
        users = [
            self.pentester2, self.pentester1, self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [
            self.user1, self.customer1, self.customer2,
            self.management2, self.management1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class TechnologyCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('api:backend:technology-list')
        self.data = {
            'name': 'technology 1'
        }

    def test_allowed(self):
        users = [
            self.pentester2, self.pentester1, self.read_only1
        ]
        for user in users:
            self.data['name'] = self.data['name'] + user.username
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        users = [
            self.user1, self.customer1, self.customer2,
            self.management2, self.management1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)
