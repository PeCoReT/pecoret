from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models import CompanyInformation


class CompanyInformationCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:companies:information-list", company=self.project1.company.pk)
        self.data = {"text": "test123"}
        self.users_allowed = [
            self.pentester1, self.management1, self.read_only1, self.management2, self.customer1,
            self.pentester2
        ]
        self.users_forbidden = [
            self.user1, self.customer2
        ]

    def test_allowed(self):
        for user in self.users_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_api_token_allowed(self):
        for user in self.users_allowed:
            self.api_token_check(user, 'scope_companies', self.url, self.client.post, 403, 201, 403, data=self.data)

    def test_api_token_forbidden(self):
        for user in self.users_forbidden:
            self.api_token_check(user, 'scope_companies', self.url, self.client.post, 403, 403, 403, data=self.data)

    def test_forbidden(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)


class CompanyInformationDestroyView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.company_information = self.create_instance(CompanyInformation, company=self.project1.company)
        self.company_information2 = self.create_instance(CompanyInformation, company=self.project2.company)
        self.url = self.get_url("api:backend:companies:information-detail",
                                company=self.project1.company.pk,
                                pk=self.company_information.pk)

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_pentester(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_pentester2(self):
        self.client.force_login(self.pentester2)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_read_only(self):
        self.client.force_login(self.read_only1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_idor(self):
        self.url = self.get_url("api:backend:companies:information-detail",
                                company=self.project1.company.pk, pk=self.company_information2.pk)
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 404)

    def test_forbidden(self):
        users = [self.user1, self.customer2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)


class CompanyInformationListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:companies:information-list", company=self.project1.company.pk)
        self.users_allowed = [
            self.pentester1, self.read_only1, self.management2, self.management1, self.customer1, self.pentester2
        ]
        self.users_forbidden = [
            self.user1, self.customer2
        ]

    def test_allowed(self):
        for user in self.users_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_api_token_allowed(self):
        for user in self.users_allowed:
            self.api_token_check(user, 'scope_companies', self.url, self.client.get, 200, 200, 403)

    def test_api_token_forbidden(self):
        for user in self.users_forbidden:
            self.api_token_check(user, 'scope_companies', self.url, self.client.get, 403, 403, 403)


class CompanyInformationUpdateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
