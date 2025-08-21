from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase

from attack_surface.scanning.models import ScanTemplate, ScanBatchRequest
from attack_surface.scanning.models.scan_batch import StatusChoices
from attack_surface.tests.mixin import AttackSurfaceMixin


class ScanTemplateRateLimitTests(AttackSurfaceMixin, APITestCase):
    def setUp(self):
        self.init_mixin()
        self.template1 = self.create_instance(ScanTemplate, rate_limit=5, enabled=True, cooldown=timedelta(seconds=0))
        self.template2 = self.create_instance(ScanTemplate, rate_limit=2, enabled=True, cooldown=timedelta(seconds=0))
        self.template3 = self.create_instance(ScanTemplate, rate_limit=3, enabled=False, cooldown=timedelta(seconds=0))

        # Create some ScanBatchRequest objects for these templates
        for i in range(4):
            self.create_instance(ScanBatchRequest, scan_template=self.template1, status=StatusChoices.PENDING,
                                 batch_end_time=timezone.now())
        for i in range(3):
            self.create_instance(ScanBatchRequest, scan_template=self.template2, status=StatusChoices.PENDING,
                                 batch_end_time=timezone.now())
        # Simulate a ScanBatchRequest for a disabled template
        self.create_instance(ScanBatchRequest, scan_template=self.template3, status=StatusChoices.PENDING,)

    def test_rate_limit_checked(self):
        # Query scan templates and apply the rate_limit_checked filter
        allowed_templates = ScanTemplate.objects.rate_limit_checked()

        # Verify that:
        # - template1 has 4 batches, so it should still be allowed (rate limit of 5)
        # - template2 has 3 batches, so it should be excluded (rate limit of 2)
        # - template3 is disabled, so it should be excluded automatically
        self.assertIn(self.template1, allowed_templates)  # Template 1 should be included
        self.assertNotIn(self.template2, allowed_templates)  # Template 2 should be excluded (rate limit exceeded)
