from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models.project_file import ProjectFile


class ProjectFileCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:file-list", project=self.project1.pk)
        self.data = {}

    def test_allowed(self):
        users = [
            self.pentester1, self.management1
        ]
        for user in users:
            self.data["name"] = f"file-{user.username}"
            self.data["file"] = SimpleUploadedFile("test.pdf", b"asdf", content_type="application/pdf")
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data, format="multipart")

    def test_traversal(self):
        self.client.force_login(self.pentester1)
        self.data = {
            "name": "test",
            "file": SimpleUploadedFile("../test.pdf", b"asdf", content_type="application/pdf")
        }
        response = self.basic_status_code_check(self.url, self.client.post, 201, data=self.data,
                                                format="multipart")
        self.assertIn("files", response.json()["file"])

    def test_forbidden(self):
        users = [
            self.pentester2, self.read_only1, self.management2, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data, format="multipart")


class ProjectFileDestroyView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.file1 = self.create_instance(ProjectFile, project=self.project1)
        self.file2 = self.create_instance(ProjectFile, project=self.project2)
        self.url = self.get_url("api:backend:file-detail", project=self.project1.pk, pk=self.file1.pk)

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_forbidden(self):
        users = [
            self.user1, self.read_only1, self.pentester2, self.management2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)

    def test_idor(self):
        self.client.force_login(self.pentester1)
        self.url = self.get_url("api:backend:file-detail", project=self.project1.pk, pk=self.file2.pk)
        self.basic_status_code_check(self.url, self.client.delete, 404)


class ProjectFileRetrieveView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()


class ProjectFileUpdateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
