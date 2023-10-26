from rest_framework.test import APITestCase
from backend.models.report_templates import ReportTemplate, ReportTemplateStatus
from pecoret.core.test import PeCoReTTestCaseMixin


class ReportTemplateListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:report-template-list")
        self.report_template1 = self.create_instance(
            ReportTemplate, status=ReportTemplateStatus.DRAFT
        )

    def test_show_only_active(self):
        self.client.force_login(self.superuser)
        response = self.basic_status_code_check(self.url, self.client.get, 200)
        self.assertEqual(response.json()["count"], 2)

        # check non-superuser
        self.client.force_login(self.pentester1)
        response = self.basic_status_code_check(self.url, self.client.get, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(
            response.json()["results"][0]["pk"],
            ReportTemplate.objects.get(name="default_template").pk,
        )
        template = response.json()["results"][0]
        self.assertIsNone(template.get("path"))


class ReportTemplateCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:report-template-list")
        self.data = {
            "name": "test",
            "package": "test",
            "status": ReportTemplateStatus.ACTIVE.label,
        }

    def test_allowed(self):
        self.client.force_login(self.superuser)
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        users = [
            self.pentester1,
            self.pentester2,
            self.read_only1,
            self.management1,
            self.management2,
            self.advisory_manager1,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 403, data=self.data
            )


class ReportTemplateUpdateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.report_template = self.create_instance(ReportTemplate)
        self.url = self.get_url(
            "backend:report-template-detail", pk=self.report_template.pk
        )
        self.data = {"path": "newtmppath"}

    def test_allowed(self):
        self.client.force_login(self.superuser)
        self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)

    def test_forbidden(self):
        users = [
            self.pentester1,
            self.pentester2,
            self.read_only1,
            self.user1,
            self.management1,
            self.management2,
            self.advisory_manager1,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.patch, 403, data=self.data
            )


class ReportTemplateDestroyView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.report_template = self.create_instance(ReportTemplate)
        self.url = self.get_url(
            "backend:report-template-detail", pk=self.report_template.pk
        )

    def test_allowed(self):
        self.client.force_login(self.superuser)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_forbidden(self):
        users = [
            self.pentester1,
            self.pentester2,
            self.read_only1,
            self.user1,
            self.management1,
            self.management2,
            self.advisory_manager1,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)
