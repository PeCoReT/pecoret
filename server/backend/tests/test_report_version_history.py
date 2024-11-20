from rest_framework.test import APITestCase

from backend.models import Report, ChangeHistory
from pecoret.core.test import PeCoReTTestCaseMixin


class ReportHistoryListViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.history1 = self.create_instance(
            ChangeHistory, report__project=self.project1
        )
        self.history2 = self.create_instance(
            ChangeHistory, report__project=self.project2
        )
        self.url = self.get_url(
            "api:backend:change-history-list",
            project=self.project1.pk,
            report=self.history1.report.pk,
        )

    def test_allowed(self):
        users = [self.pentester1, self.management1, self.read_only1]
        for user in users:
            self.client.force_login(user)
            response = self.basic_status_code_check(self.url, self.client.get, 200)
            self.assertEqual(response.json()["count"], 1)

    def test_forbidden(self):
        users = [self.pentester2, self.management2, self.user1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_broken_access(self):
        self.client.force_login(self.pentester1)
        url = self.get_url(
            "api:backend:change-history-list",
            project=self.project1.pk,
            report=self.history2.report.pk,
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class ReportHistoryCreateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.report1 = self.create_instance(Report, project=self.project1)
        self.report2 = self.create_instance(Report, project=self.project2)
        self.url1 = self.get_url(
            "api:backend:change-history-list",
            project=self.project1.pk,
            report=self.report1.pk,
        )
        self.data = {
            "change": "test",
            "user": self.pentester1.pk,
            "version": "0.1",
            "date": "2022-01-01",
        }

    def test_allowed(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url1, self.client.post, 201, data=self.data)

    def test_allowed_management(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url1, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        users = [self.pentester2, self.management2, self.user1, self.read_only1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url1, self.client.post, 403, data=self.data
            )

    def test_broken_access(self):
        url = self.get_url(
            "api:backend:change-history-list",
            project=self.project1.pk,
            report=self.report2.pk,
        )
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(
            url, self.client.post, 403, data=self.data
        )


class ReportHistoryUpdateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.history1 = self.create_instance(
            ChangeHistory, report__project=self.project1
        )
        self.history2 = self.create_instance(
            ChangeHistory, report__project=self.project2
        )
        self.url = self.get_url(
            "api:backend:change-history-detail",
            project=self.project1.pk,
            report=self.history1.report.pk,
            pk=self.history1.pk,
        )
        self.data = {"version": "1.2"}

    def test_forbidden(self):
        users = [self.read_only1, self.user1, self.management2, self.pentester2]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.patch, 403, data=self.data
            )

    def test_allowed(self):
        users = [self.pentester1, self.management1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.patch, 200, data=self.data
            )

    def test_broken_access(self):
        url = self.get_url(
            "api:backend:change-history-detail",
            project=self.project1.pk,
            report=self.history2.report.pk,
            pk=self.history2.pk,
        )
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(url, self.client.patch, 403, data=self.data)
        url = self.get_url(
            "api:backend:change-history-detail",
            project=self.project1.pk,
            report=self.history1.report.pk,
            pk=self.history2.pk,
        )
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(url, self.client.patch, 404, data=self.data)
        url = self.get_url(
            "api:backend:change-history-detail",
            project=self.project1.pk,
            report=self.history2.report.pk,
            pk=self.history1.pk,
        )
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(url, self.client.patch, 403, data=self.data)


class ReportHistoryDestroyViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.history1 = self.create_instance(
            ChangeHistory, report__project=self.project1
        )
        self.history2 = self.create_instance(
            ChangeHistory, report__project=self.project2
        )
        self.url = self.get_url(
            "api:backend:change-history-detail",
            project=self.project1.pk,
            report=self.history1.report.pk,
            pk=self.history1.pk,
        )

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_forbidden(self):
        users = [self.management2, self.pentester2, self.read_only1, self.user1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)

    def test_broken_access(self):
        url = self.get_url(
            "api:backend:change-history-detail",
            project=self.project1.pk,
            report=self.history1.report.pk,
            pk=self.history2.pk,
        )
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(url, self.client.delete, 404)

        url = self.get_url(
            "api:backend:change-history-detail",
            project=self.project1.pk,
            report=self.history2.report.pk,
            pk=self.history1.pk,
        )
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(url, self.client.delete, 403)

        url = self.get_url(
            "api:backend:change-history-detail",
            project=self.project2.pk,
            report=self.history1.report.pk,
            pk=self.history1.pk,
        )
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(url, self.client.delete, 403)

        url = self.get_url(
            "api:backend:change-history-detail",
            project=self.project1.pk,
            report=self.history2.report.pk,
            pk=self.history2.pk,
        )
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(url, self.client.delete, 403)
