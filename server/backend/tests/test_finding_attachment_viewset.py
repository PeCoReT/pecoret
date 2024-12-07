import base64

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase

from backend.models import FindingImageAttachment
from pecoret.core.test import PeCoReTTestCaseMixin


class ImageAttachmentListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.finding1 = self.create_finding(
            project=self.project1,
            asset=self.asset1,
            user=self.pentester1,
            vulnerability__project=self.project1,
        )
        self.finding2 = self.create_finding(
            project=self.project2,
            asset=self.asset2,
            user=self.pentester2,
            vulnerability__project=self.project2,
        )
        self.proof1 = self.create_instance(FindingImageAttachment, finding=self.finding1)
        self.proof2 = self.create_instance(FindingImageAttachment, finding=self.finding2)
        self.url = self.get_url(
            "api:backend:findings:attachment-list",
            project=self.project1.pk,
            finding=self.finding1.pk,
        )
        self.users_allowed = [
            self.pentester1, self.management1, self.read_only1
        ]
        self.users_forbidden = [
            self.user1, self.pentester2, self.customer1, self.customer2
        ]

    def test_allowed_status(self):
        for user in self.users_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden_status(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_api_token_allowed(self):
        for user in self.users_allowed:
            self.api_token_check(user, 'scope_all_projects', self.url, self.client.get, 200, 200, 403)

    def test_api_token_forbidden(self):
        for user in self.users_forbidden:
            self.api_token_check(user, 'scope_all_projects', self.url, self.client.get, 403, 403, 403)

    def test_idor(self):
        self.client.force_login(self.pentester1)
        url = self.get_url(
            "api:backend:findings:attachment-list",
            project=self.project2.pk,
            finding=self.finding1.pk,
        )
        self.basic_status_code_check(url, self.client.get, 403)
        url = self.get_url(
            "api:backend:findings:attachment-list",
            project=self.project1.pk,
            finding=self.finding2.pk,
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class AttachmentCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.finding1 = self.create_finding(
            project=self.project1,
            asset=self.asset1,
            user=self.pentester1,
            vulnerability__project=self.project1,
        )
        self.finding2 = self.create_finding(
            project=self.project2,
            asset=self.asset2,
            user=self.pentester2,
            vulnerability__project=self.project2,
        )
        self.url = self.get_url(
            "api:backend:findings:attachment-list",
            project=self.project1.pk,
            finding=self.finding1.pk,
        )
        self.image64 = ("iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAA"
                        "O9TXL0Y4OHwAAAABJRU5ErkJggg==")
        self.data = {
            "caption": "proof1",
        }
        self.users_allowed = [
            self.pentester1, self.management1
        ]
        self.users_forbidden = [
            self.pentester2, self.read_only1, self.user1, self.management2,
            self.customer1, self.customer2
        ]

    def test_allowed(self):
        for user in self.users_allowed:
            self.client.force_login(user)
            self.data["image"] = SimpleUploadedFile("file.png", base64.b64decode(self.image64),
                                                    content_type="image/png")
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data,
                                         format="multipart")

    def test_forbidden(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 403, data=self.data, format="multipart"
            )


class ProofDestroyViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.finding1 = self.create_finding(
            project=self.project1,
            asset=self.asset1,
            user=self.pentester1,
            vulnerability__project=self.project1,
        )
        self.finding2 = self.create_finding(
            project=self.project2,
            asset=self.asset2,
            user=self.pentester2,
            vulnerability__project=self.project2,
        )
        self.proof1 = self.create_instance(FindingImageAttachment, finding=self.finding1)
        self.proof2 = self.create_instance(FindingImageAttachment, finding=self.finding2)
        self.url = self.get_url(
            "api:backend:findings:attachment-detail",
            project=self.project1.pk,
            pk=self.proof1.pk,
            finding=self.finding1.pk,
        )

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204, data={})

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.delete, 204, data={})

    def test_forbidden(self):
        users = [self.management2, self.read_only1, self.user1, self.pentester2]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403, data={})
