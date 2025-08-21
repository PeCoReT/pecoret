from datetime import timedelta

from rest_framework.test import APITestCase

from attack_surface.scanning.models import ScanTemplate
from pecoret.core.test import PeCoReTTestCaseMixin


class ScanTemplateListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('api:attack_surface:scan-template-list')

        self.allowed_users = [
            self.pentester1,
            self.pentester2,
            self.read_only1,
        ]

        self.forbidden_users = [
            self.management1,
            self.management2,
            self.user1,
            self.customer1,
            self.customer2
        ]

    def test_allowed_users_cannot_see_scanner_config(self):
        self.create_instance(ScanTemplate, name="Test Template", scanner_config={"foo": "bar"},
                             cooldown=timedelta(minutes=1))

        for user in self.allowed_users:
            self.client.force_login(user)
            response = self.basic_status_code_check(self.url, self.client.get, 200)
            # Check that `scanner_config` is not included in any of the items in the response JSON
            for item in response.json():
                self.assertNotIn('scanner_config', item)

    def test_forbidden_users(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)
