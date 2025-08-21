from django.utils import timezone
from rest_framework.test import APITestCase

from advisories.models.advisory import Severity, Advisory
from advisories.models.label import Label
from advisories.models.share_token import ShareToken
from backend.models import VulnerabilityTemplate, CWE, Technology
from pecoret.core.test import PeCoReTTestCaseMixin


class AdvisoryListViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:advisories:advisory-list")
        self.allowed_users = [self.pentester1, self.pentester2, self.read_only1]
        self.forbidden_users = [
            self.management1,
            self.management2,
            self.customer1,
            self.customer2,
            self.user1,
        ]

    def test_status_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_api_token_allowed(self):
        for user in self.allowed_users:
            self.api_token_check(
                user, "scope_advisories", self.url, self.client.get, 200, 200, 403
            )

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_api_token_forbidden(self):
        users = [self.user1]
        for user in users:
            self.api_token_check(
                user, "scope_advisories", self.url, self.client.get, 403, 403, 403
            )


class AdvisoryCreateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:advisories:advisory-list")
        self.cwe = self.create_instance(CWE)
        self.tech = self.create_instance(Technology)
        self.data = {
            "technology": self.tech.pk,
            "affected_versions": "1.0",
            "fixed_version": None,
            "report_template": "default_template",
            "severity": Severity.LOW.label,
            "description": "lorem ipsum",
            "proofs": "lorem ipsum",
            "recommendation": "lorem ipsum",
            "cwes": [self.cwe.pk],
            "title": "test",
            "labels": [],
        }
        self.users_forbidden = [
            self.user1,
            self.customer1,
            self.customer2,
            self.management2,
            self.management1,
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
            self.api_token_check(
                user,
                "scope_advisories",
                self.url,
                self.client.post,
                403,
                403,
                403,
                data=self.data,
            )

    def test_allowed(self):
        for user in self.users_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 201, data=self.data
            )

    def test_api_token_allowed(self):
        for user in self.users_allowed:
            self.api_token_check(
                user,
                "scope_advisories",
                self.url,
                self.client.post,
                403,
                201,
                403,
                data=self.data,
            )


class AdvisoryUpdateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:advisories:advisory-detail", pk=self.advisory1.pk)
        self.url2 = self.get_url("api:advisories:advisory-detail", pk=self.advisory2.pk)
        self.cwe = self.create_instance(CWE)
        self.data = {"product": "new product", "cwes": [self.cwe.pk]}
        self.allowed_users = [self.pentester1, self.pentester2, self.read_only1]
        self.forbidden_users = [
            self.customer1,
            self.customer2,
            self.management1,
            self.management2,
            self.user1,
        ]

    def test_status_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.patch, 200, data=self.data
            )
            self.assertEqual(
                Advisory.objects.filter(cwes=self.cwe).exists(),
                True,
            )

    def test_status_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.patch, 403, data=self.data
            )

    def test_label(self):
        self.client.force_login(self.pentester1)
        label = self.create_instance(Label, color="#111111")
        self.data["labels"] = [label.pk]
        self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)
        self.assertEqual(
            Advisory.objects.filter(
                pk=self.advisory1.pk, labels__in=[label.pk]
            ).count(),
            1,
        )


class AdvisoryDestroyViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:advisories:advisory-detail", pk=self.advisory1.pk)
        self.url2 = self.get_url("api:advisories:advisory-detail", pk=self.advisory2.pk)
        self.user_forbidden = [self.management2, self.management1, self.user1]

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


class AdvisoryShareTokenDownload(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.token = ShareToken.objects.create(
            date_expire=timezone.now() + timezone.timedelta(days=2),
            advisory=self.advisory1,
        )
        self.url = self.get_url(
            "api:advisories:advisory-download-with-token",
            pk=self.advisory1.pk,
            share_token=self.token.token,
        )

    def test_allowed(self):
        self.basic_status_code_check(self.url, self.client.get, 200)

    def test_expired(self):
        self.token.date_expire = timezone.now() - timezone.timedelta(days=2)
        self.token.save()
        self.basic_status_code_check(self.url, self.client.get, 404)

    def test_broken_access(self):
        self.url = self.get_url(
            "api:advisories:advisory-download-with-token",
            pk=self.advisory2.pk,
            share_token=self.token.token,
        )
        self.basic_status_code_check(self.url, self.client.get, 404)
