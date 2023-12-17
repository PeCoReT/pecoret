from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from checklists.models import Category, Item


class ItemListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('checklists:item-list')
        item = self.create_instance(Item)

    def test_allowed(self):
        users = [
            self.pentester2, self.pentester1, self.management2, self.management1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [
            self.advisory_manager1, self.user1, self.vendor2, self.vendor1, self.read_only_vendor
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class ItemCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('checklists:item-list')
        category = self.create_instance(Category)
        self.data = {
            'item_id': 'test',
            'name': 'test',
            'description': 'asdf',
            'category': category.pk
        }

    def test_allowed(self):
        users = [
            self.pentester2, self.pentester1
        ]
        for user in users:
            self.data['item_id'] = self.data['item_id'] + user.username
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        users = [
            self.management1, self.management2, self.advisory_manager1, self.vendor1,
            self.vendor2, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)
