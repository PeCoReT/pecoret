from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models.project_contact import ProjectContact
from backend.models.company_contact import CompanyContact


class ProjectContactListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.contact1 = self.create_instance(ProjectContact, project=self.project1)
        self.contact2 = self.create_instance(ProjectContact, project=self.project2)
        self.url = self.get_url("api:backend:contact-list", project=self.project1.pk)

    def test_allowed(self):
        users = [
            self.pentester1, self.management1, self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            response = self.basic_status_code_check(self.url, self.client.get, 200)
            self.assertEqual(response.json()["count"], 1)
            self.assertEqual(response.json()["results"][0]["pk"], self.contact1.pk)

    def test_forbidden(self):
        users = [
            self.pentester2, self.management2, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class ProjectContactCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.company_contact1 = self.create_instance(CompanyContact, company=self.project1.company)
        self.company_contact2 = self.create_instance(CompanyContact, company=self.project2.company)
        self.url = self.get_url("api:backend:contact-list", project=self.project1.pk)
        self.data = {"contact": self.company_contact1.pk}

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        users = [
            self.pentester2, self.management2, self.read_only1, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)

    def test_broken_access(self):
        self.client.force_login(self.pentester1)
        self.data["contact"] = self.company_contact2.pk
        self.basic_status_code_check(self.url, self.client.post, 400, data=self.data)


class ProjectContactDestroyView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.contact1 = self.create_instance(ProjectContact, project=self.project1)
        self.url = self.get_url("api:backend:contact-detail", project=self.project1.pk, pk=self.contact1.pk)

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_forbidden(self):
        users = [
            self.read_only1, self.user1, self.management2, self.pentester2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)


class ProjectContactUpdateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.company_contact1 = self.create_instance(CompanyContact, company=self.project1.company)
        self.company_contact2 = self.create_instance(CompanyContact, company=self.project2.company)
        self.contact1 = self.create_instance(ProjectContact, project=self.project1, contact=self.company_contact1)
        self.contact2 = self.create_instance(ProjectContact, project=self.project2, contact=self.company_contact2)
        self.url = self.get_url("api:backend:contact-detail", project=self.project1.pk, pk=self.contact1.pk)
        self.data = {"contact": self.company_contact1.pk}

    def test_allowed(self):
        users = [
            self.management1, self.pentester1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)

    def test_forbidden(self):
        users = [
            self.management2, self.pentester2, self.read_only1, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)

    def test_broken_access(self):
        self.data = {"contact": self.company_contact2.pk}
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.patch, 400, data=self.data)
