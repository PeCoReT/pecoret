from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models.project import ProjectStatus, TestMethod
from backend.models.pentest_type import PentestType


class ProjectListViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:project-list")

    def test_status_code(self):
        self.client.force_login(self.pentester1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        j = response.json()
        self.assertEqual(j["count"], 1)
        self.assertEqual(j["results"][0]["pk"], self.project1.pk)

    def test_read_only(self):
        self.client.force_login(self.read_only1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        j = response.json()
        self.assertEqual(j["count"], 1)
        self.assertEqual(j["results"][0]["pk"], self.project1.pk)

    def test_customer(self):
        self.client.force_login(self.customer1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        j = response.json()
        self.assertEqual(j["count"], 0)

    def test_pentester2(self):
        self.client.force_login(self.pentester2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        j = response.json()
        self.assertEqual(j["count"], 1)
        self.assertEqual(j["results"][0]["pk"], self.project2.pk)

    def test_management(self):
        self.client.force_login(self.management1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        j = response.json()
        self.assertEqual(j["count"], 1)
        self.assertEqual(j["results"][0]["pk"], self.project1.pk)

    def test_no_group(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class ProjectDestroyViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:project-detail", pk=self.project1.pk)

    def test_permissions(self):
        user_status_map = [
            (self.pentester1, 403),
            (self.management1, 204),
            (self.pentester2, 403),
            (self.user1, 403),
            (self.read_only1, 403),
        ]
        self.basic_permission_checks(self.url, user_status_map, self.client.delete)


class ProjectDetailViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:project-detail", pk=self.project1.pk)

    def test_permissions(self):
        user_status_map = [
            (self.pentester1, 200),
            (self.management1, 200),
            (self.pentester2, 403),
            (self.read_only1, 200),
            (self.user1, 403),
        ]
        self.basic_permission_checks(self.url, user_status_map, self.client.get)


class ProjectCreateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:project-list")
        self.pentest_types = [
            PentestType.objects.create(name="Web").pk,
            PentestType.objects.create(name="Network").pk,
        ]
        self.data = {
            "name": "test",
            "status": ProjectStatus.OPEN.label,
            "language": "English",
            "start_date": "2022-02-02",
            "company": 1,
            "test_method": TestMethod.BLACK_BOX.label,
            "pentest_types": self.pentest_types,
            "end_date": "2022-02-02",
            "description": "test",
        }

    def test_allowed(self):
        users = [self.management1, self.management2]
        for user in users:
            self.data["name"] = self.data["name"] + f"_{user.username}"
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 201, data=self.data
            )

    def test_forbidden(self):
        users = [
            self.pentester1,
            self.pentester2,
            self.read_only1,
            self.user1,
            self.advisory_manager1,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 403, data=self.data
            )


class PinProjectViewSet(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:project-pin-project", pk=self.project1.pk)

    def test_forbidden(self):
        users = [
            self.read_only1, self.management2, self.pentester2,
            self.advisory_manager1, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403)

    def test_allowed(self):
        users = [
            self.pentester1, self.management1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201)


class UnpinProjectViewSet(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:project-pin-project", pk=self.project1.pk)

    def test_forbidden(self):
        users = [
            self.read_only1, self.management2, self.pentester2,
            self.advisory_manager1, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)

    def test_allowed(self):
        users = [
            self.pentester1, self.management1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 204)
