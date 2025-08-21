from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase

from attack_surface.models import Program, Scanner, ScanFinding
from pecoret.core.test import PeCoReTTestCaseMixin


class ScanFindingCreateUpdateView(PeCoReTTestCaseMixin, APITestCase):
    def setUp(self):
        self.init_mixin()
        self.scanner = self.create_instance(Scanner)
        self.program = self.create_instance(Program)
        self.url = self.get_url("api:attack_surface:scan-finding-create-or-update")
        self.data = {
            'affected_component': 'http://localhost',
            'name': 'Test Vuln',
            'severity': 'Critical',
            'program': self.program.pk,
            'result': 'test',
            'tool': 'Test',
        }

    def test_create(self):
        headers = {'X-Scanner-Auth': self.scanner.token}
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data, headers=headers)
        self.assertEqual(ScanFinding.objects.count(), 1)

    def test_ignore_until(self):
        headers = {'X-Scanner-Auth': self.scanner.token}
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data, headers=headers)
        self.assertEqual(ScanFinding.objects.count(), 1)
        finding = ScanFinding.objects.first()
        finding.ignore_until = timezone.now() + timedelta(days=10)
        finding.save()
        self.data['result'] = 'invalid'
        self.basic_status_code_check(self.url, self.client.post, 200, data=self.data, headers=headers)
        self.assertEqual(ScanFinding.objects.filter(result="test").count(), 1)
