from rest_framework.test import APITestCase
from backend.models import Finding
from pecoret.core.test import PeCoReTTestCaseMixin


class CVSSBaseScoreList(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.finding1 = self.create_finding(
            project=self.project1,
            component=self.asset1,
            user=self.pentester1,
            vulnerability__project=self.project1,
        )
        self.finding2 = self.create_finding(
            project=self.project2,
            component=self.asset2,
            user=self.pentester2,
            vulnerability__project=self.project2,
        )
        self.url = self.get_url(
            "backend:findings:cvss-score-list",
            project=self.project1.pk,
            finding=self.finding1.pk,
        )

    def test_allowed(self):
        users = [self.management1, self.read_only1, self.pentester1]
        for user in users:
            self.client.force_login(user)
            response = self.basic_status_code_check(self.url, self.client.get, 200)
            self.assertEqual(response.json()["pk"], self.finding1.cvssbasescore.pk)

    def test_forbidden(self):
        users = [self.management2, self.pentester2, self.user1, self.advisory_manager1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_broken_access(self):
        self.url = self.get_url(
            "backend:findings:cvss-score-list",
            project=self.project1.pk,
            finding=self.finding2.pk,
        )
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.get, 403)


class CVSSBaseScoreUpdate(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()


class CVSS40CalculatorView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url("backend:cvss4-calculator")
        self.data = {
            'vector': 'CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:N/SC:L/SI:N/SA:N'
        }

    def test_cvss4_calculator(self):
        self.client.force_login(self.pentester1)
        response = self.basic_status_code_check(self.url, self.client.post, 200, data=self.data)
        self.assertEqual(response.json()['score'], 5.3)
        self.assertEqual(response.json()['severity'], 'Medium')
