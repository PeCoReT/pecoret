from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models.project_scope import ProjectScope, ScopePermission


class ProjectScopeListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.scope1 = self.create_instance(ProjectScope, project=self.project1)
        self.url = self.get_url("api:backend:scope-list", project=self.project1.pk)

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


class ProjectScopeUpdateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.scope1 = self.create_instance(ProjectScope, project=self.project1)
        self.url = self.get_url("api:backend:scope-detail", project=self.project1.pk, pk=self.scope1.pk)
        self.data = {
            "details": "Test access allowed",
            "permission": ScopePermission.ALLOWED.label
        }

    def test_allowed(self):
        users = [
            self.pentester1, self.management1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)

    def test_forbidden(self):
        users = [
            self.management2, self.pentester2, self.user1, self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)


class ProjectScopeCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.scope1 = self.create_instance(ProjectScope, project=self.project1)
        self.url = self.get_url("api:backend:scope-list", project=self.project1.pk)
        self.data = {
            "details": "Test access allowed",
            "permission": ScopePermission.ALLOWED.label
        }

    def test_allowed(self):
        users = [
            self.pentester1, self.management1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        users = [
            self.management2, self.pentester2, self.user1, self.read_only1,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)


class ProjectScopeDeleteView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.scope1 = self.create_instance(ProjectScope, project=self.project1)
        self.url = self.get_url("api:backend:scope-detail", project=self.project1.pk, pk=self.scope1.pk)

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_forbidden(self):
        users = [
            self.pentester2, self.user1, self.read_only1, self.management2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)
