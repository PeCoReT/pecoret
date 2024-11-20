from rest_framework.test import APITestCase

from backend.models.company_contact import CompanyContact
from pecoret.core.test import PeCoReTTestCaseMixin


class CompanyContactListViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.company = self.project1.company
        self.url = self.get_url("api:backend:companies:contact-list", company=self.company.pk)
        self.users_allowed = [
            self.management1, self.management2, self.pentester1, self.read_only1, self.customer1, self.pentester2
        ]
        self.users_forbidden = [
            self.user1, self.customer2
        ]

    def test_allowed(self):
        for user in self.users_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_api_token_allowed(self):
        for user in self.users_allowed:
            self.api_token_check(user, 'scope_companies', self.url, self.client.get, 200, 200, 403)

    def test_forbidden(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_api_token_forbidden(self):
        for user in self.users_forbidden:
            self.api_token_check(user, 'scope_companies', self.url, self.client.get, 403, 403, 403)


class CompanyContactDeleteViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.company_contact = self.create_instance(CompanyContact)
        self.url = self.get_url("api:backend:companies:contact-detail", company=self.company_contact.company.pk,
                                pk=self.company_contact.pk)
        self.users_forbidden = [
            self.user1, self.customer2, self.customer1
        ]

    def test_management2(self):
        self.client.force_login(self.management2)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_pentester2(self):
        self.client.force_login(self.pentester2)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_api_token_management1(self):
        self.api_token_check(self.management1, 'scope_companies', self.url, self.client.delete, 403, 204, 403)

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_forbidden(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)

    def test_api_token_forbidden(self):
        for user in self.users_forbidden:
            self.api_token_check(user, 'scope_companies', self.url, self.client.delete, 403, 403, 403)


class CompanyContactUpdateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.company_contact = self.create_instance(CompanyContact)
        self.url = self.get_url("api:backend:companies:contact-detail", company=self.company_contact.company.pk,
                                pk=self.company_contact.pk)
        self.data = {"last_name": "fromtest"}

    def test_allowed(self):
        users = [
            self.management1, self.management2, self.pentester2, self.pentester1, self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)

    def test_customer(self):
        self.client.force_login(self.customer1)
        self.company_contact = self.create_instance(CompanyContact, company=self.project1.company)
        self.url = self.get_url('api:backend:companies:contact-detail', company=self.project1.company.pk,
                                pk=self.company_contact.pk)
        self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)

    def test_forbidden(self):
        users = [
            self.user1, self.customer2, self.customer1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)

    def test_idor(self):
        company_contact2 = self.create_instance(CompanyContact, company=self.project2.company)
        self.url = self.get_url('api:backend:companies:contact-detail', company=self.project1.company.pk,
                                pk=company_contact2.pk)
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.patch, 404, data=self.data)
