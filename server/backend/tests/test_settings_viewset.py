from rest_framework.test import APITestCase
from extra_settings.models import Setting
from pecoret.core.test import PeCoReTTestCaseMixin


class SettingsPatchView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        setting = Setting.objects.get(name='GENERAL_COMPANY_NAME')
        self.url = self.get_url('backend:setting-detail', pk=setting.pk)
        self.data = {'setting_value': 'test1231234'}

    def test_allowed(self):
        self.client.force_login(self.superuser)
        self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)
        setting = Setting.get('GENERAL_COMPANY_NAME')
        self.assertEqual(setting, self.data['setting_value'])

    def test_forbidden(self):
        users = [
            self.pentester1, self.pentester2, self.user1, self.read_only1,
            self.vendor1, self.vendor2, self.read_only_vendor, self.management2, self.management1,
            self.advisory_manager1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)


class SettingsListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('backend:setting-list')

    def test_allowed(self):
        self.client.force_login(self.superuser)
        self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [
            self.pentester1, self.pentester2, self.user1, self.read_only1,
            self.vendor1, self.vendor2, self.read_only_vendor, self.management2, self.management1,
            self.advisory_manager1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)
