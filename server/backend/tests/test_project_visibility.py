from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models.project import Visibility


class ProjectListVisibility(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.public_project = self.create_project()
        self.public_project.visibility = Visibility.PENTESTERS
        self.public_project.save()
        self.allowed_users = [
            self.pentester1, self.pentester2, self.read_only1
        ]
        self.non_public_users = [
            self.management1, self.management2
        ]
        self.url = self.get_url('backend:project-list')

    def test_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            response = self.basic_status_code_check(self.url, self.client.get, 200)
            self.assertEqual(response.json()['count'], 2)

    def test_non_public_permissions(self):
        for user in self.non_public_users:
            self.client.force_login(user)
            response = self.basic_status_code_check(self.url, self.client.get, 200)
            self.assertEqual(response.json()['count'], 1)


class ProjectDetailVisibility(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.public_project = self.create_project()
        self.public_project.visibility = Visibility.PENTESTERS
        self.public_project.save()
        self.allowed_users = [
            self.pentester1, self.pentester2, self.read_only1
        ]
        self.non_public_users = [
            self.management1, self.management2
        ]
        self.url = self.get_url('backend:project-detail', pk=self.public_project.pk)

    def test_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_non_public_permissions(self):
        for user in self.non_public_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class ProjectUpdateVisibility(APITestCase, PeCoReTTestCaseMixin):
    """
    test which users are allowed to change visibility
    """
    def setUp(self):
        self.init_mixin()
        self.public_project = self.create_project()
        self.public_project.visibility = Visibility.PENTESTERS
        self.public_project.save()
        self.allowed_users = [
            self.management2, self.management1
        ]
        self.not_allowed = [
            self.pentester1, self.pentester2, self.read_only1,
        ]
        self.url = self.get_url('backend:project-detail', pk=self.public_project.pk)
        self.data = {
            'visibility': Visibility.MEMBERS_ONLY.label
        }

    def test_not_allowed(self):
        for user in self.not_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 400, data=self.data, debug=True)

    def test_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)
            self.public_project.visibility = Visibility.PENTESTERS
            self.public_project.save()
