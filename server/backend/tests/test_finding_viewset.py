from rest_framework.test import APITestCase
from django.core import mail
from backend.models import (
    VulnerabilityTemplate,
    Advisory,
    ProjectVulnerability,
    ReportTemplate
)
from backend.models.finding import FindingStatus, Severity
from backend.models.account import Account
from backend.models.advisory import VisibilityChoices
from pecoret.core.test import PeCoReTTestCaseMixin


class FindingListViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.finding1 = self.create_finding(
            project=self.project1,
            vulnerability__project=self.project1,
            component=self.asset1,
            user=self.pentester1,
        )
        self.finding2 = self.create_finding(
            project=self.project2,
            vulnerability__project=self.project2,
            component=self.asset2,
            user=self.pentester2,
        )
        self.url = self.get_url("backend:finding-list", project=self.project1.pk)

    def test_status_allowed(self):
        users = [self.read_only1, self.pentester1, self.management1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_status_forbidden(self):
        users = [self.user1, self.management2, self.pentester2]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_project(self):
        self.client.force_login(self.pentester1)
        response = self.client.get(self.url)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["pk"], self.finding1.pk)

    def test_filter_component_valid(self):
        self.client.force_login(self.pentester1)
        self.url = f"{self.url}?{self.asset1.asset_type}={self.asset1.pk}"
        response = self.client.get(self.url)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["pk"], self.finding1.pk)

    def test_filter_component_invalid(self):
        self.client.force_login(self.pentester1)
        self.url = f"{self.url}?{self.asset2.asset_type}={self.asset2.pk}"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)


class FindingCreateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:finding-list", project=self.project1.pk)
        self.create_instance(VulnerabilityTemplate, vulnerability_id="path-traversal")
        self.data = {
            "name": "testfinding",
            "severity": Severity.CRITICAL.label,
            "status": FindingStatus.OPEN.label,
            "recommendation": "",
            "proof_text": "test",
            "imported": False,
            "component": {"type": "web_application", "pk": self.asset1.pk},
            "vulnerability_id": "path-traversal",
        }
        self.pentester1.usersettings.notify_critical_findings = True
        self.pentester1.usersettings.save()

    def test_allowed(self):
        users = [self.pentester1, self.management1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 201, data=self.data
            )
        # this is two, because two critical findings will be created. one for management1 and one for pentester1
        self.assertEqual(len(mail.outbox), 2)

    def test_forbidden(self):
        users = [self.pentester2, self.user1, self.management2]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 403, data=self.data
            )

    def test_foreign_asset(self):
        data = self.data
        data["component"]["pk"] = self.asset2.pk
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 400, data=self.data)

    def test_account_assignment(self):
        account1 = self.create_instance(Account, project=self.project1)
        account2 = self.create_instance(Account, project=self.project2)
        self.data["user_account"] = account1.pk
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)
        self.data["user_account"] = account2.pk
        self.basic_status_code_check(self.url, self.client.post, 400, data=self.data)


class FindingUpdateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.finding1 = self.create_finding(
            project=self.project1,
            vulnerability__project=self.project1,
            component=self.asset1,
            user=self.pentester1,
        )
        self.finding2 = self.create_finding(
            project=self.project2,
            vulnerability__project=self.project2,
            component=self.asset2,
            user=self.pentester2,
        )
        self.url = self.get_url(
            "backend:finding-detail", project=self.project1.pk, pk=self.finding1.pk
        )
        self.data = {"name": "finding_updated"}

    def test_allowed(self):
        users = [self.pentester1, self.management1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.patch, 200, data=self.data
            )

    def test_forbidden(self):
        users = [self.pentester2, self.management2, self.read_only1, self.user1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.patch, 403, data=self.data
            )

    def test_foreign_finding(self):
        url = self.get_url(
            "backend:finding-detail", project=self.project1.pk, pk=self.finding2.pk
        )
        self.client.force_login(self.pentester1)
        response = self.client.patch(url, self.data, format="json")
        self.assertEqual(response.status_code, 404)

    def test_foreign_project(self):
        url = self.get_url(
            "backend:finding-detail", project=self.project1.pk, pk=self.finding2.pk
        )
        self.client.force_login(self.pentester1)
        response = self.client.patch(url, self.data, format="json")
        self.assertEqual(response.status_code, 404)


class FindingDestroyViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.finding1 = self.create_finding(
            project=self.project1,
            vulnerability__project=self.project1,
            component=self.asset1,
            user=self.pentester1,
        )
        self.url = self.get_url(
            "backend:finding-detail", project=self.project1.pk, pk=self.finding1.pk
        )

    def test_status_allowed(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_pentester_allowed(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_status_forbidden(self):
        users = [self.pentester2, self.user1, self.read_only1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)


class FindingAsAdvisoryView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.template = self.create_instance(VulnerabilityTemplate)
        self.project_vulnerability = self.create_instance(
            ProjectVulnerability,
            project=self.project1,
            vulnerability_id=self.template.vulnerability_id,
        )
        self.finding1 = self.create_finding(
            project=self.project1,
            component=self.asset1,
            user=self.pentester1,
            vulnerability=self.project_vulnerability,
        )
        self.url = self.get_url(
            "backend:finding-as-advisory", project=self.project1.pk, pk=self.finding1.pk
        )
        self.data = {
            "product": "Test Product",
            "vendor_url": "https://asdfasdf.com",
            "vendor_name": "Test Vendor",
            "affected_versions": "234.2",
        }

    def test_function(self):
        advisory = Advisory.objects.create_from_finding(self.finding1, **self.data)
        self.assertIsNotNone(advisory)

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)
        # there is already one created during `setUp`
        self.assertEqual(Advisory.objects.filter(visibility=VisibilityChoices.MEMBERS).count(), 2)

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)
        # there is already one created during `setUp`
        self.assertEqual(Advisory.objects.filter(visibility=VisibilityChoices.MEMBERS).count(), 2)

    def test_forbidden(self):
        users = [
            self.pentester2,
            self.management2,
            self.user1,
            self.read_only1,
            self.advisory_manager1,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 403, data=self.data
            )


class TestFindingPDFExportView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.report_template = ReportTemplate.objects.get(name="default_template")
        self.template = self.create_instance(VulnerabilityTemplate)
        self.project_vulnerability = self.create_instance(
            ProjectVulnerability,
            project=self.project1,
            vulnerability_id=self.template.vulnerability_id,
        )
        self.finding1 = self.create_finding(
            project=self.project1,
            component=self.asset1,
            user=self.pentester1,
            vulnerability=self.project_vulnerability,
        )
        self.url = self.get_url(
            "backend:finding-export-pdf", project=self.project1.pk, pk=self.finding1.pk
        )

    def test_allowed(self):
        users = [self.pentester1, self.management1, self.read_only1]
        for user in users:
            self.client.force_login(user)
            response = self.basic_status_code_check(self.url, self.client.get, 200)
            self.assertIn("Content-Disposition", response.headers)

    def test_forbidden(self):
        users = [self.pentester2, self.advisory_manager1, self.management2, self.user1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)
