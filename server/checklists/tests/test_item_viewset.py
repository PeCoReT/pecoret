from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from checklists.models import Category, Item


class ItemListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('api:checklists:item-list')
        self.users_allowed = [
            self.pentester2, self.pentester1, self.management1, self.management2, self.read_only1
        ]
        self.users_forbidden = [
            self.user1, self.customer1, self.customer2
        ]

    def test_allowed(self):
        for user in self.users_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_api_token_allowed(self):
        for user in self.users_allowed:
            self.api_token_check(user, 'scope_knowledgebase', self.url, self.client.get, 200, 200 ,403)

    def test_api_token_forbidden(self):
        for user in self.users_forbidden:
            self.api_token_check(user, 'scope_knowledgebase', self.url, self.client.get, 403, 403, 403)


class ItemCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('api:checklists:item-list')
        category = self.create_instance(Category)
        self.data = {
            'item_id': 'test',
            'name': 'test',
            'description': 'asdf',
            'category': category.pk
        }
        self.users_allowed = [
            self.pentester2, self.pentester1, self.read_only1
        ]
        self.users_forbidden = [
            self.customer2, self.customer1, self.user1,
            self.management1, self.management2
        ]

    def test_allowed(self):
        for user in self.users_allowed:
            self.data['item_id'] = user.username
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)

    def test_api_token_allowed(self):
        for user in self.users_allowed:
            self.data['item_id'] = user.username
            self.api_token_check(user, 'scope_knowledgebase', self.url, self.client.post, 403, 201, 403, data=self.data)

    def test_api_token_forbidden(self):
        for user in self.users_forbidden:
            self.api_token_check(user, 'scope_knowledgebase', self.url, self.client.post, 403, 403, 403, data=self.data)
