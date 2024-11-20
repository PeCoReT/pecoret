from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models import Service, Host


class ServiceCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:service-list", project=self.project1.pk)
        self.host1 = self.create_instance(Host, project=self.project1)
        self.host2 = self.create_instance(Host, project=self.project2)
        self.data = {
            "host": self.host1.pk, "name": "http", "port": 80, "product": "Apache", "protocol": "TCP", "state": "Open"
        }

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        users = [
            self.read_only1, self.pentester2, self.user1, self.management2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)

    def test_broken_access(self):
        self.data["host"] = self.host2.pk
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 400, data=self.data)


class ServiceListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.host1 = self.create_instance(Host, project=self.project1)
        self.host2 = self.create_instance(Host, project=self.project2)
        self.service1 = self.create_instance(Service, host=self.host1)
        self.service2 = self.create_instance(Service, host=self.host2)
        self.url = self.get_url("api:backend:service-list", project=self.project1.pk)

    def test_allowed(self):
        users = [
            self.read_only1, self.management1, self.pentester1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [
            self.management2, self.pentester2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_filter_allowed(self):
        self.client.force_login(self.pentester1)
        response = self.client.get(self.url + f"?host={self.host1.pk}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["pk"], self.service1.pk)

    def test_filter_forbidden(self):
        self.client.force_login(self.pentester1)
        response = self.client.get(self.url + f"?host={self.host2.pk}")
        self.assertEqual(response.status_code, 400)


class ServiceUpdateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.host1 = self.create_instance(Host, project=self.project1)
        self.host2 = self.create_instance(Host, project=self.project2)
        self.service1 = self.create_instance(Service, host=self.host1)
        self.service2 = self.create_instance(Service, host=self.host2)
        self.url = self.get_url("api:backend:service-detail", project=self.project1.pk, pk=self.service1.pk)
        self.data = {"name": "https"}

    def test_allowed(self):
        users = []
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 200)

    def test_forbidden(self):
        users = [
            self.read_only1, self.management2, self.pentester2, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)

    def test_broken_access(self):
        self.data["host"] = self.host2.pk
        self.data["port"] = "80"
        self.data["protocol"] = "TCP"
        self.data["state"] = "Open"
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.patch, 400, data=self.data)

    def test_invalid_service(self):
        self.url = self.get_url("api:backend:service-detail", project=self.project1.pk, pk=self.service2.pk)
        self.data["port"] = "80"
        self.data["protocol"] = "TCP"
        self.data["state"] = "Open"
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.patch, 404, data=self.data)


class ServiceDestroyView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.host1 = self.create_instance(Host, project=self.project1)
        self.host2 = self.create_instance(Host, project=self.project2)
        self.service1 = self.create_instance(Service, host=self.host1)
        self.service2 = self.create_instance(Service, host=self.host2)
        self.url = self.get_url("api:backend:service-detail", project=self.project1.pk, pk=self.service1.pk)

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_forbidden(self):
        users = [
            self.read_only1, self.management2, self.pentester2, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)
