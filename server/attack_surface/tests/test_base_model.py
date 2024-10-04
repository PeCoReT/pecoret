from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from attack_surface.models import Target, ScanObject, ScanType
from attack_surface.models.scan import Scan, ScanStatus
from pecoret.core.test import PeCoReTTestCaseMixin


class RunningScanTargetDeletion(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.target = self.create_instance(Target, data='example.com')
        scan_type = self.create_instance(ScanType, allowed_object_type='target')
        self.scan = self.create_instance(Scan, status=ScanStatus.RUNNING, scan_type=scan_type)
        self.scan_object = self.create_instance(ScanObject, content_type=ContentType.objects.get_for_model(Target),
                                                scan=self.scan,
                                                object_id=self.target.pk)

    def test_running_deletion(self):
        with self.assertRaises(ValidationError):
            self.target.delete()
