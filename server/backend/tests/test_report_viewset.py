from django.conf import settings
from rest_framework.test import APITestCase

from backend.models.reports.report import Report
from pecoret.core.test import PeCoReTTestCaseMixin


class ReportListViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:report-list", project=self.project1.pk)

    def test_allowed(self):
        users = [
            self.pentester1, self.management1, self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [
            self.pentester2, self.user1, self.management2, self.customer1, self.customer2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class ReportCreateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:report-list", project=self.project1.pk)
        self.report_template = list(settings.REPORT_TEMPLATES.keys())[0]
        self.data = {
            "name": "Test",
            "title": "Test Report",
            "project": self.project1.pk,
            "language": "English",
            "recommendation": "",
            "evaluation": "",
            "template": self.report_template
        }

    def test_inactive_report_template(self):
        self.data["template"] = "i-do-not-exist-really-just-for-testing"
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 400, data=self.data)

    def test_allowed(self):
        users = [
            self.pentester1, self.management1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        users = [
            self.pentester2, self.read_only1, self.user1, self.customer1, self.customer2, self.management2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)


class ReportUpdateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.report1 = self.create_instance(
            Report,
            project=self.project1,
            template=list(settings.REPORT_TEMPLATES.keys())[0]
        )
        self.url = self.get_url(
            "api:backend:report-detail", project=self.project1.pk, pk=self.report1.pk
        )
        self.data = {"name": "test2"}

    def test_allowed(self):
        users = [
            self.pentester1, self.management1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)

    def test_forbidden(self):
        users = [
            self.pentester2, self.management2, self.read_only1,
            self.customer1, self.customer2, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)


class ReportDeleteViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.report1 = self.create_instance(Report, project=self.project1)
        self.url = self.get_url(
            "api:backend:report-detail", project=self.project1.pk, pk=self.report1.pk
        )

    def test_pentester(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_forbidden(self):
        users = [
            self.pentester2, self.user1, self.read_only1,
            self.customer1, self.management2, self.customer2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)

    def test_management(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.delete, 204)


class ReportDetailViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    # TODO: implement
    pass
