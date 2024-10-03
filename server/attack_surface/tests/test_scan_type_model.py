from rest_framework.test import APITestCase

from attack_surface.models import ScanType, Target
from pecoret.core.test import PeCoReTTestCaseMixin


class ScanTypeQuerySetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.st1 = self.create_instance(ScanType, allowed_object_type='target')
        self.st2 = self.create_instance(ScanType, allowed_object_type='target')
        self.st3 = self.create_instance(ScanType, allowed_object_type='service')
        self.target = self.create_instance(Target, data='example.com')

    def test_for_asset_query(self):
        qs = ScanType.objects.for_asset(self.target)
        self.assertEqual(qs.count(), 2)
