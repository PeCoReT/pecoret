from rest_framework.test import APITestCase

from backend.models import ObjectLock
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models.project_note import ProjectNote


class ProjectNoteListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.note = self.create_instance(ProjectNote, project=self.project1)
        self.url = self.get_url('api:backend:note-list', project=self.project1.pk)

    def test_allowed(self):
        users = [
            self.pentester1, self.management1, self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [
            self.management2, self.pentester2, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class ProjectNoteCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('api:backend:note-list', project=self.project1.pk)
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
            self.read_only1, self.management2,
            self.pentester2, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)


class ProjectNoteUpdateView(APITestCase, PeCoReTTestCaseMixin):
    pass


class ProjectNoteDeleteView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.note = self.create_instance(ProjectNote, project=self.project1)
        self.lock = ObjectLock.objects.create(locked_object=self.note, object_id=self.note.pk, user=self.pentester1)
        self.url = self.get_url('api:backend:note-detail', project=self.project1.pk, pk=self.note.pk)

    def test_locked(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 400)
        self.lock.delete()
        self.basic_status_code_check(self.url, self.client.delete, 204)
