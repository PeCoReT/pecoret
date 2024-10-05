from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from attack_surface.models import Finding
from attack_surface.models.finding import ProgressStatus
from pecoret.core.test import PeCoReTTestCaseMixin


class FindingStatusTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.finding = self.create_instance(Finding, description=None, status=ProgressStatus.DRAFT)

    def test_change_status(self):
        with self.assertRaises(ValidationError):
            self.finding.status = ProgressStatus.FINAL
            self.finding.save()
