from rest_framework.test import APITestCase

from attack_surface.models import ScanType, Host
from pecoret.core.test import PeCoReTTestCaseMixin


class ScanTypeQuerySetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.st1 = self.create_instance(ScanType, allowed_object_type='host')
        self.st2 = self.create_instance(ScanType, allowed_object_type='host')
        self.st3 = self.create_instance(ScanType, allowed_object_type='service')
        self.host = self.create_instance(Host)

    def test_for_asset_query(self):
        qs = ScanType.objects.for_asset(self.host)
        self.assertEqual(qs.count(), 2)
