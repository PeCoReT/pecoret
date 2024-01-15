from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models.report_templates import ReportTemplate
from backend.models.advisory import VisibilityChoices


class AdvisoryExportViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.report_template = ReportTemplate.objects.get(name="default_template")
        self.url = self.get_url("advisories:advisory-export-pdf", pk=self.advisory1.pk)

    def test_allowed(self):
        users = [
            self.pentester1,
            self.vendor1,
            self.advisory_manager1,
            self.read_only_vendor,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [
            self.management1,
            self.management2,
            self.user1,
            self.vendor2,
            self.read_only1,
            self.pentester2,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_management_draft(self):
        self.advisory1.visibility = VisibilityChoices.MEMBERS
        self.advisory1.save()
        self.client.force_login(self.advisory_manager1)
        self.basic_status_code_check(self.url, self.client.get, 403)
