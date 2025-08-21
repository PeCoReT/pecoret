from django.conf import settings
from rest_framework.test import APITestCase
from backend.models import Report, ReportRelease
from backend.models.reports.report_release import ReleaseType
from pecoret.core.test import PeCoReTTestCaseMixin


class ReportDocumentListTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.report1 = self.create_instance(Report, project=self.project1)
        self.report2 = self.create_instance(Report, project=self.project2)
        self.document1 = self.create_instance(ReportRelease, report=self.report1)
        self.document2 = self.create_instance(ReportRelease, report=self.report2)
        self.url = self.get_url(
            "api:backend:report-release-list",
            project=self.project1.pk,
            report=self.report1.pk,
        )

    def test_output_listview(self):
        self.client.force_login(self.pentester1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["pk"], self.document1.pk)

    def test_management_status_code(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.get, 200)

    def test_pentester2_status_code(self):
        self.client.force_login(self.pentester2)
        self.basic_status_code_check(self.url, self.client.get, 403)

    def test_read_only_status_code(self):
        self.client.force_login(self.read_only1)
        self.basic_status_code_check(self.url, self.client.get, 200)

    def test_user1_status_code(self):
        self.client.force_login(self.user1)
        self.basic_status_code_check(self.url, self.client.get, 403)


class ReportDocumentUpdateTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.report1 = self.create_instance(Report, project=self.project1)
        self.report2 = self.create_instance(Report, project=self.project2)
        self.document1 = self.create_instance(ReportRelease, report=self.report1)
        self.document2 = self.create_instance(ReportRelease, report=self.report2)
        self.url = self.get_url(
            "api:backend:report-release-detail",
            project=self.project1.pk,
            report=self.report1.pk,
            pk=self.document1.pk,
        )

    def test_pentester1_status(self):
        self.client.force_login(self.pentester1)
        data = {"name": "123test"}
        self.basic_status_code_check(self.url, self.client.patch, 405, data=data)


class ReportDocumentCreateTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.report_template = list(settings.REPORT_TEMPLATES.keys())[0]
        self.report1 = self.create_instance(Report, project=self.project1, template=self.report_template)
        self.report2 = self.create_instance(Report, project=self.project2, template=self.report_template)
        self.url = self.get_url(
            "api:backend:report-release-list",
            project=self.project1.pk,
            report=self.report1.pk,
        )
        self.data = {
            "name": "test",
            "release_type": ReleaseType.DRAFT.label,
        }

    def test_non_existent_template(self):
        with self.settings(REPORT_TEMPLATES={'default_template': {}, 'i-do-not-exist': {}}):
            self.report1.template = 'i-do-not-exist'
            self.report1.save()
        users = [
            self.pentester1, self.management1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 400, data=self.data)
        self.report1.template = 'default_template'
        self.report1.save()

    def test_pentester1_status(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)
        self.assertEqual(ReportRelease.objects.filter(report=self.report1).count(), 1)

    def test_forbidden_status(self):
        self.client.force_login(self.pentester2)
        self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)
        self.client.force_login(self.user1)
        self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)

    def test_management1_status(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.post, 201, self.data)


class ReportDocumentDownloadTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.report1 = self.create_instance(Report, project=self.project1)
        self.report2 = self.create_instance(Report, project=self.project2)
        self.document1 = self.create_instance(
            ReportRelease, report=self.report1, compiled_source=b"document1"
        )
        self.document2 = self.create_instance(
            ReportRelease, report=self.report2, compiled_source=b"document2"
        )
        self.url = self.get_url(
            "api:backend:report-release-download",
            project=self.project1.pk,
            report=self.report1.pk,
            pk=self.document1.pk,
        )

    def test_allowed_status(self):
        for user in [self.read_only1, self.pentester1, self.management1]:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden_status(self):
        for user in [self.pentester2, self.user1]:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_uri_tempering(self):
        url = self.get_url(
            "api:backend:report-release-download",
            project=self.project1.pk,
            report=self.report2.pk,
            pk=self.document1.pk,
        )
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(url, self.client.get, 403)
        url = self.get_url(
            "api:backend:report-release-download",
            project=self.project1.pk,
            report=self.report1.pk,
            pk=self.document2.pk,
        )
        self.basic_status_code_check(url, self.client.get, 404)


class ReportPreviewDocument(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.report1 = self.create_instance(Report, project=self.project1, template='default_template')
        self.url = self.get_url("api:backend:report-release-list", project=self.project1.pk, report=self.report1.pk)
        self.data = {"release_type": "Preview", "name": "Preview"}

    def test_unique_preview_document(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)
        self.data["name"] = "second"
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)
        self.assertEqual(ReportRelease.objects.for_report(self.report1).count(), 1)
        release = ReportRelease.objects.for_report(self.report1).get()
        self.assertEqual(release.name, self.data["name"])
