from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models.project_note import ProjectNote


class ProjectNoteListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.note = self.create_instance(ProjectNote, project=self.project1)
        self.url = self.get_url('backend:note-list', project=self.project1.pk)

    def test_allowed(self):
        users = [
            self.pentester1, self.management1, self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [
            self.vendor1, self.vendor2, self.management2, self.advisory_manager1,
            self.pentester2, self.user1, self.read_only_vendor
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class ProjectNoteCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('backend:note-list', project=self.project1.pk)
        self.data = {
            'title': 'Test'
        }

    def test_allowed(self):
        users = [
            self.pentester1, self.management1
        ]
        for user in users:
            self.data['title'] = f"{self.data['title']}{user.username}"
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        users = [
            self.read_only1, self.vendor2, self.vendor1, self.management2, self.advisory_manager1,
            self.pentester2, self.user1, self.read_only_vendor
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)


class ProjectNoteUpdateView(APITestCase, PeCoReTTestCaseMixin):
    pass


class ProjectNoteDeleteView(APITestCase, PeCoReTTestCaseMixin):
    pass
