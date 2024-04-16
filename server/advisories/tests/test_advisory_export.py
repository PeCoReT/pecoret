from rest_framework.test import APITestCase

from advisories.models.advisory import VisibilityChoices
from backend.models.report_templates import ReportTemplate
from pecoret.core.test import PeCoReTTestCaseMixin


class AdvisoryExportViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.report_template = ReportTemplate.objects.get(name="default_template")
        self.url = self.get_url("advisories:advisory-export-pdf", pk=self.advisory1.pk)
        self.users_allowed = [
            self.pentester1,
            self.vendor1,
            self.advisory_manager1,
            self.read_only_vendor,
        ]
        self.users_forbidden = [self.management1,
                                self.management2,
                                self.user1,
                                self.customer1, self.customer2,
                                self.management1, self.management2,
                                self.vendor2,
                                self.read_only1,
                                self.pentester2, ]

    def test_allowed(self):
        for user in self.users_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_api_token_allowed(self):
        for user in self.users_allowed:
            self.api_token_check(user, 'scope_advisories', self.url, self.client.get, 200, 200, 403)

    def test_api_token_forbidden(self):
        for user in self.users_forbidden:
            self.api_token_check(user, 'scope_advisories', self.url, self.client.get, 403, 403, 403)

    def test_management_draft(self):
        self.advisory1.visibility = VisibilityChoices.MEMBERS
        self.advisory1.save()
        self.client.force_login(self.advisory_manager1)
        self.basic_status_code_check(self.url, self.client.get, 403)
        self.api_token_check(self.advisory_manager1, 'scope_advisories', self.url, self.client.get, 403, 403, 403)
