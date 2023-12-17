from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from checklists.models import Category


class CategoryListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('checklists:category-list')
        self.category = self.create_instance(Category)

    def test_allowed(self):
        users = [
            self.pentester1, self.pentester2,
            self.management1, self.management2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [
            self.advisory_manager1, self.vendor1, self.vendor2, self.user1,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class CategoryCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('checklists:category-list')
        self.data = {
            'category_id': 'test123',
            'name': 'test',
            'summary': 'asdf'
        }

    def test_allowed(self):
        users = [
            self.pentester1, self.pentester2
        ]
        for user in users:
            self.client.force_login(user)
            self.data['category_id'] = self.data['category_id'] + user.username
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        users = [
            self.management1, self.management2, self.read_only_vendor, self.vendor1,
            self.vendor2, self.advisory_manager1, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)
