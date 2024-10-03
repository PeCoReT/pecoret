from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APITestCase

from attack_surface.models import ScanType, Target, Scan, ScanObject
from attack_surface.models.scan import ScanStatus
from pecoret.core.test import PeCoReTTestCaseMixin


class ScanCreateViewSet(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('attack_surface:scan-list')
        self.scan_type = self.create_instance(ScanType, allowed_object_type='target')
        self.scan_type2 = self.create_instance(ScanType, allowed_object_type='service')
        self.host = self.create_instance(Target, data='example.com')
        self.data = {
            'name': 'test', 'scan_type': self.scan_type.pk,
            'scan_objects': [{'content_type': 'target', 'object_id': self.host.pk}]
        }
        self.allowed_users = [self.pentester2, self.pentester1, self.read_only1]
        self.forbidden_users = [self.management1, self.management2, self.customer1, self.customer2, self.vendor1,
                                self.vendor2, self.user1]

    def test_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.data['name'] = user.username
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)

    def test_invalid_type(self):
        self.data['scan_type'] = self.scan_type2.pk
        self.client.force_login(self.pentester1)
        response = self.basic_status_code_check(self.url, self.client.post, 400, data=self.data)
        self.assertEqual(len(response.json().get('target', [])), 1)
        self.assertIn("Expected 'service'", response.json()['target'][0])

    def test_object_not_exist(self):
        self.data['scan_objects'][0]['object_id'] = 1000
        self.client.force_login(self.pentester1)
        response = self.basic_status_code_check(self.url, self.client.post, 400, data=self.data)
        self.assertEqual(len(response.json().get('scan_objects', [])), 1)

    def test_missing_object(self):
        self.data['scan_objects'] = []
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 400, data=self.data)


class ScanUpdateDeleteView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.scan_type = self.create_instance(ScanType, allowed_object_type='target')
        self.scan_type2 = self.create_instance(ScanType, allowed_object_type='service')
        self.host = self.create_instance(Target, data='test.example.com')
        self.host2 = self.create_instance(Target, data='example.com')
        self.scan = self.create_instance(Scan, scan_type=self.scan_type)
        ct = ContentType.objects.get_for_model(self.host)
        self.scan_object = self.create_instance(ScanObject, scan=self.scan, content_type=ct, object_id=self.host.pk)
        self.data = {}
        self.url = self.get_url('attack_surface:scan-detail', pk=self.scan.pk)

    def test_cannot_change_scan_objects(self):
        self.data['scan_type'] = self.scan_type2.pk
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)
        scan = Scan.objects.get(pk=self.scan.pk)
        self.assertEqual(self.scan_type.pk, scan.scan_type.pk)

    def test_delete_non_pending_scan(self):
        self.scan.status = ScanStatus.RUNNING
        self.scan.save()
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 400)
        self.assertEqual(Scan.objects.filter(pk=self.scan.pk).count(), 1)
