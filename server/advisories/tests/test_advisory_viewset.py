from rest_framework.test import APITestCase

from advisories.models.advisory import Severity, Advisory
from advisories.models.label import Label
from backend.models import VulnerabilityTemplate, Technology
from pecoret.core.test import PeCoReTTestCaseMixin


class AdvisoryListViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("advisories:advisory-list")
        self.allowed_users = [self.pentester1, self.pentester2, self.read_only1]
        self.forbidden_users = [self.management1, self.management2, self.customer1, self.customer2, self.user1,
                                self.vendor1, self.vendor2]

    def test_status_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_api_token_allowed(self):
        for user in self.allowed_users:
            self.api_token_check(user, 'scope_advisories', self.url, self.client.get, 200, 200, 403)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_api_token_forbidden(self):
        users = [self.user1]
        for user in users:
            self.api_token_check(user, 'scope_advisories', self.url, self.client.get, 403, 403, 403)


class AdvisoryCreateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("advisories:advisory-list")
        self.tech = self.create_instance(Technology)
        self.create_instance(VulnerabilityTemplate, vulnerability_id="path-traversal")
        self.data = {
            "technology": self.tech.pk,
            "affected_versions": "1.0",
            "fixed_version": None,
            "report_template": "default_template",
            "severity": Severity.LOW.label,
            "description": "lorem ipsum",
            "proofs": "lorem ipsum",
            "recommendation": "lorem ipsum",
            "vulnerability_id": "path-traversal",
            "title": "test",
            "labels": []
        }
        self.users_forbidden = [
            self.user1, self.vendor1, self.vendor2, self.customer1, self.customer2, self.management2, self.management1
        ]
        self.users_allowed = [self.pentester1, self.read_only1, self.pentester2]

    def test_forbidden(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 403, data=self.data
            )

    def test_api_token_forbidden(self):
        for user in self.users_forbidden:
            self.api_token_check(user, 'scope_advisories', self.url, self.client.post, 403, 403, 403, data=self.data)

    def test_allowed(self):
        for user in self.users_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 201, data=self.data
            )

    def test_api_token_allowed(self):
        for user in self.users_allowed:
            self.api_token_check(user, 'scope_advisories', self.url, self.client.post, 403, 201, 403, data=self.data)


class AdvisoryUpdateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("advisories:advisory-detail", pk=self.advisory1.pk)
        self.url2 = self.get_url("advisories:advisory-detail", pk=self.advisory2.pk)
        self.template = self.create_instance(VulnerabilityTemplate, vulnerability_id='new-test-vulnerability')
        self.data = {"product": "new product", "vulnerability_id": self.template.vulnerability_id}
        self.allowed_users = [self.pentester1, self.pentester2, self.read_only1]
        self.forbidden_users = [self.customer1, self.customer2, self.management1, self.management2, self.vendor1,
                                self.vendor2, self.user1]

    def test_status_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.patch, 200, data=self.data
            )
            self.assertEqual(Advisory.objects.filter(
                vulnerability__vulnerability_id='new-test-vulnerability').exists(), True)

    def test_status_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)

    def test_label(self):
        self.client.force_login(self.pentester1)
        label = self.create_instance(Label, color="#111111")
        self.data["labels"] = [label.pk]
        self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)
        self.assertEqual(Advisory.objects.filter(pk=self.advisory1.pk, labels__in=[label.pk]).count(), 1)

    def test_label_forbidden(self):
        self.client.force_login(self.vendor1)
        label = self.create_instance(Label, color="#111111")
        self.data["labels"] = [label.pk]
        self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)
        self.assertEqual(Advisory.objects.filter(pk=self.advisory1.pk, labels__in=[label.pk]).count(), 0)


class AdvisoryDestroyViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("advisories:advisory-detail", pk=self.advisory1.pk)
        self.url2 = self.get_url("advisories:advisory-detail", pk=self.advisory2.pk)
        self.user_forbidden = [
            self.management2, self.management1, self.user1, self.vendor1, self.vendor2,
        ]

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_pentester2(self):
        self.client.force_login(self.pentester2)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_status_forbidden(self):
        for user in self.user_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)
