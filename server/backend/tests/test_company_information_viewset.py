from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin, AdvisoryTestCaseMixin
from backend.models import CompanyInformation


class CompanyInformationCreateView(APITestCase, AdvisoryTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:company-information-list")
        self.data = {"company": self.project1.company.pk, "text": "test123"}

    def test_allowed(self):
        users = [
            self.pentester1, self.management1, self.pentester2, self.read_only1, self.management2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        users = [
            self.vendor1, self.vendor2, self.user1, self.advisory_manager1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)


class CompanyInformationDestroyView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.company_information = self.create_instance(CompanyInformation, company=self.project1.company)
        self.url = self.get_url("backend:company-information-detail", pk=self.company_information.pk)

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_pentester(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_forbidden(self):
        users = [
            self.advisory_manager1, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)


class CompanyInformationListView(APITestCase, AdvisoryTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:company-information-list")

    def test_allowed(self):
        users = [
            self.pentester1, self.pentester2, self.read_only1, self.management2, self.management1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [
            self.user1, self.advisory_manager1, self.vendor1, self.vendor2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class CompanyInformationUpdateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
