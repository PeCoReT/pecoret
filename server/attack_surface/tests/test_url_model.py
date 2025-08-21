from rest_framework.test import APITestCase

from attack_surface.models import URL, Service, Target
from attack_surface.models.target import DataTypes
from backend.models import Technology
from pecoret.core.test import PeCoReTTestCaseMixin


class TestTechnologySync(PeCoReTTestCaseMixin, APITestCase):
    def setUp(self):
        self.init_mixin()

    def test_url_technology_sync(self):
        target = self.create_instance(Target, data="example.com", data_type=DataTypes.DOMAIN)
        url = self.create_instance(URL, service__target=target, service__port_number=80, service__service_name="http")
        technology = self.create_instance(Technology)
        url.technologies.add(technology)
        url.save()
        self.assertEqual(Service.objects.filter(technologies=technology).count(), 1)
