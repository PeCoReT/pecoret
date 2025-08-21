from rest_framework.test import APITestCase
from django.core.management import call_command


class ManagementCommandTestCase(APITestCase):
    def test_cronjobs(self):
        call_command('init_default_cronjobs')

    def test_sampledata(self):
        call_command('sampledata')

    def test_import_cwe(self):
        call_command('import_cwe_entries')
