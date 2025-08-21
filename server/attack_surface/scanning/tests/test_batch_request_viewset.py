from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase

from attack_surface.models import Scanner, Program, Target
from attack_surface.scanning.models import ScanTemplate, ScanBatchRequest
from attack_surface.scanning.models.scan_batch import StatusChoices
from attack_surface.tests.mixin import AttackSurfaceMixin
from pecoret.core.test import PeCoReTTestCaseMixin


class ScannerPollingTest(AttackSurfaceMixin, APITestCase):
    def setUp(self):
        self.init_mixin()
        self.scanner = self.create_instance(Scanner)
        self.url = self.get_url('api:attack_surface:scan-request-fetch-next-scan')

    def test_allowed(self):
        headers = {'X-Scanner-Auth': self.scanner.token}
        resp = self.basic_status_code_check(self.url, self.client.get, 200, headers=headers)
        self.assertEqual(resp.json(), {})

    def test_scan_batch_within_cooldown_is_excluded(self):
        # Create a scan batch that is within the cooldown period (e.g., scanned within the last 24 hours)
        scan_template = self.create_instance(ScanTemplate, cooldown=timedelta(days=1), rate_limit=None)
        scan_batch = self.create_instance(ScanBatchRequest, scan_template=scan_template,
                                          batch_end_time=timezone.now() - timedelta(hours=12))

        headers = {'X-Scanner-Auth': self.scanner.token}

        # Try to fetch the scan batch
        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {})

    def test_scan_batch_respects_rate_limit(self):
        # Create a scan batch with rate limit set in its template
        # TODO: create multiple batches with same template and template threshold of 1 (allowed to run once a day)
        # fetch 2 batches, first one should be 200 with batch in response, other one 204
        pass

    def test_missing_auth_header_returns_403(self):
        # Call the API without the authentication header
        response = self.client.get(self.url)

        # Ensure the response is 403 Forbidden
        self.assertEqual(response.status_code, 403)

    def test_scan_batch_is_marked_in_progress_when_fetched(self):
        # Create a scan batch and simulate fetching it
        scan_template = self.create_instance(ScanTemplate, rate_limit=None, cooldown=timedelta(seconds=0))
        scan_batch = self.create_instance(ScanBatchRequest, scan_template=scan_template, status=StatusChoices.PENDING)

        headers = {'X-Scanner-Auth': self.scanner.token}

        # Fetch the scan batch
        response = self.client.get(self.url, headers=headers)

        # Ensure the response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Ensure the scan batch status has been updated to 'in-progress'
        scan_batch.refresh_from_db()
        self.assertEqual(scan_batch.status, StatusChoices.IN_PROGRESS)


class ScanBatchRequestListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.program = self.create_instance(Program)
        self.target = self.create_instance(Target, data="example.com")

        self.url = self.get_url('api:attack_surface:scan-request-list')

        self.allowed_users = [
            self.pentester1,
            self.pentester2,
            self.read_only1
        ]

        self.forbidden_users = [
            self.management1,
            self.management2,
            self.user1,
            self.customer1,
            self.customer2
        ]

    def test_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class ScanBatchRequestCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.program = self.create_instance(Program)
        self.target = self.create_instance(Target, data="example.com")
        self.url = self.get_url('api:attack_surface:scan-request-list')

        self.allowed_users = [
            self.pentester1,
            self.pentester2,
            self.read_only1
        ]

        self.forbidden_users = [
            self.management1,
            self.management2,
            self.user1,
            self.customer1,
            self.customer2
        ]

    def test_not_implemented_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403)


class ScanBatchRequestUpdateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.batch = self.create_instance(ScanBatchRequest, scan_template__cooldown=timedelta(seconds=0))
        self.url = self.get_url('api:attack_surface:scan-request-detail', pk=self.batch.pk)

        self.allowed_users = [
            self.pentester1,
            self.pentester2,
            self.read_only1
        ]

        self.forbidden_users = [
            self.management1,
            self.management2,
            self.user1,
            self.customer1,
            self.customer2
        ]

    def test_not_implemented_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 403)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 403)
