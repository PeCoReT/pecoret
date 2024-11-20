from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models.assets.base import Environment, AssetAccessibility
from backend.models.assets.mobile_application import MobileApplication, OperatingSystem


class MobileApplicationCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:mobile-application-list", project=self.project1.pk)
        self.data = {"accessible": AssetAccessibility.UNKNOWN.label,
                     "environment": Environment.UNKNOWN.label, "name": "testapp", "version": "1.0",
                     "certificate_pinning": True,
                     "os": OperatingSystem.UNKNOWN.label}

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        users = [self.read_only1, self.management2, self.pentester2, self.user1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)


class MobileApplicationDestroyView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.app1 = self.create_instance(MobileApplication, project=self.project1)
        self.app2 = self.create_instance(MobileApplication, project=self.project2)
        self.url = self.get_url("api:backend:mobile-application-detail", project=self.project1.pk, pk=self.app1.pk)

    def test_forbidden(self):
        users = [
            self.pentester2, self.read_only1, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_broken_access(self):
        url = self.get_url("api:backend:mobile-application-detail", project=self.project1.pk, pk=self.app2.pk)
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(url, self.client.delete, 404)


class MobileApplicationListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:mobile-application-list", project=self.project1.pk)

    def test_forbidden(self):
        users = [
            self.pentester2, self.user1, self.management2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_allowed(self):
        users = [
            self.pentester1, self.management1, self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)


class MobileApplicationUpdateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
