from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models import VulnerabilityTemplate
from backend.models.advisory import Severity, Advisory, VisibilityChoices
from advisories.models.label import Label


class AdvisoryListViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("advisories:advisory-list")

    def test_status_allowed(self):
        users = [
            self.pentester1,
            self.pentester2,
            self.advisory_manager1,
            self.read_only1,
            self.vendor1,
            self.vendor2,
            self.read_only_vendor,
            self.management1,
            self.management2,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [self.user1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_response_length(self):
        self.client.force_login(self.pentester1)
        response = self.basic_status_code_check(self.url, self.client.get, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["pk"], self.advisory1.pk)
        # test advisory management which is zero because the submission should be in inbox
        self.client.force_login(self.advisory_manager1)
        response = self.basic_status_code_check(self.url, self.client.get, 200)
        self.assertEqual(response.json()["count"], 0)

    def test_advisory_submitter_is_group_member(self):
        self.add_user_to_group(self.pentester1, "Advisory Management")
        self.client.force_login(self.pentester1)
        response = self.basic_status_code_check(self.url, self.client.get, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["pk"], self.advisory1.pk)

    def test_advisory_serializer(self):
        self.client.force_login(self.pentester1)
        response = self.basic_status_code_check(self.url, self.client.get, 200)
        self.assertEqual(response.json()["results"][0].get('labels'), None)


class AdvisoryCreateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("advisories:advisory-list")
        self.create_instance(VulnerabilityTemplate, vulnerability_id="path-traversal")
        self.data = {
            "product": "Test Product",
            "affected_versions": "1.0",
            "fixed_version": None,
            "severity": Severity.LOW.label,
            "vendor_url": "https://example.com",
            "vendor_name": "Test Vendor",
            "description": "lorem ipsum",
            "proofs": "lorem ipsum",
            "recommendation": "lorem ipsum",
            "vulnerability_id": "path-traversal",
            "internal_name": "test",
        }

    def test_forbidden(self):
        users = [
            self.user1,
            self.vendor1,
            self.vendor2,
            self.read_only_vendor,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 403, data=self.data
            )

    def test_allowed(self):
        users = [
            self.pentester1,
            self.read_only1,
            self.pentester2,
            self.advisory_manager1,
            self.management1,
            self.management2,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 201, data=self.data
            )


class AdvisoryUpdateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("advisories:advisory-detail", pk=self.advisory1.pk)
        self.url2 = self.get_url("advisories:advisory-detail", pk=self.advisory2.pk)
        self.template = self.create_instance(VulnerabilityTemplate, vulnerability_id='new-test-vulnerability')
        self.data = {"product": "new product", "vulnerability_id": self.template.vulnerability_id}

    def test_status_allowed(self):
        users = [self.advisory_manager1, self.pentester1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.patch, 200, data=self.data
            )
            self.assertEqual(Advisory.objects.filter(
                vulnerability__vulnerability_id='new-test-vulnerability').exists(), True)

    def test_draft_status(self):
        self.advisory1.visibility = VisibilityChoices.MEMBERS
        self.advisory1.save()
        self.client.force_login(self.advisory_manager1)
        self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)

    def test_status_forbidden(self):
        users = [
            self.user1,
            self.management2,
            self.management1,
            self.read_only1,
            self.read_only1,
            self.pentester2,
            self.vendor1,
            self.vendor2,
            self.read_only_vendor,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.patch, 403, data=self.data
            )

    def test_draft_allowed(self):
        users = [self.pentester2]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url2, self.client.patch, 200, data=self.data
            )

    def test_draft_forbidden(self):
        users = [
            self.vendor1,
            self.vendor2,
            self.read_only1,
            self.management1,
            self.management2,
            self.pentester1,
            self.advisory_manager1,
            self.read_only_vendor,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url2, self.client.patch, 403, data=self.data
            )

    def test_advisory_management_label(self):
        self.client.force_login(self.advisory_manager1)
        label = self.create_instance(Label, color="#111111")
        self.data["labels"] = [label.pk]
        self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)
        self.assertEqual(Advisory.objects.filter(pk=self.advisory1.pk, labels__in=[label.pk]).count(), 1)

    def test_label_forbidden(self):
        self.client.force_login(self.pentester1)
        label = self.create_instance(Label, color="#111111")
        self.data["labels"] = [label.pk]
        self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)
        self.assertEqual(Advisory.objects.filter(pk=self.advisory1.pk, labels__in=[label.pk]).count(), 0)

    def test_submitter_is_advisory_management(self):
        self.add_user_to_group(self.pentester1, "Advisory Management")
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)
        # test with draft
        draft = self.create_instance(Advisory, visibility=VisibilityChoices.MEMBERS, user=self.pentester1)
        self.url = self.get_url("advisories:advisory-detail", pk=draft.pk)
        self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)


class AdvisoryDestroyViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("advisories:advisory-detail", pk=self.advisory1.pk)
        self.url2 = self.get_url("advisories:advisory-detail", pk=self.advisory2.pk)

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_advisory_management(self):
        self.client.force_login(self.advisory_manager1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_status_forbidden(self):
        users = [
            self.management2,
            self.management1,
            self.user1,
            self.vendor1,
            self.vendor2,
            self.read_only1,
            self.pentester2,
            self.read_only_vendor,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)

    def test_draft_pentester(self):
        self.client.force_login(self.pentester2)
        self.basic_status_code_check(self.url2, self.client.delete, 204)

    def test_draft_forbidden(self):
        users = [
            self.management1,
            self.management2,
            self.user1,
            self.vendor1,
            self.vendor2,
            self.pentester1,
            self.advisory_manager1,
            self.read_only_vendor,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url2, self.client.delete, 403)
