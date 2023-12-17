from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from checklists.models import Checklist, Category


class ChecklistListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.checklist1 = self.create_instance(Checklist)
        self.url = self.get_url('checklists:checklist-list')

    def test_allowed(self):
        users = [
            self.pentester1, self.pentester2, self.read_only1,
            self.management1, self.management2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [
            self.advisory_manager1, self.user1, self.vendor1, self.vendor2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class ChecklistCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('checklists:checklist-list')
        category = self.create_instance(Category)
        self.data = {
            'checklist_id': 'test-123', 'name': 'test123', 'categories': [category.pk]
        }

    def test_allowed(self):
        users = [
            self.pentester1, self.pentester2
        ]
        for user in users:
            self.data['checklist_id'] = self.data['checklist_id'] + user.username
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        users = [
            self.management2, self.management1, self.advisory_manager1, self.user1,
            self.vendor1, self.vendor2, self.read_only_vendor
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)
