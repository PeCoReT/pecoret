from rest_framework.test import APITestCase

from backend.models import Company
from pecoret.core.test import PeCoReTTestCaseMixin


class CompanyListViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:company-list")
        self.user_allowed = [
            self.management2, self.management1, self.read_only1, self.pentester2, self.pentester1,
            self.customer1, self.customer2
        ]
        self.user_forbidden = [self.user1]

    def test_status_allowed(self):
        for user in self.user_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_api_token_allowed(self):
        for user in self.user_allowed:
            self.api_token_check(user, 'scope_companies', self.url, self.client.get, 200, 200, 403)

    def test_customer(self):
        self.client.force_login(self.customer1)
        response = self.basic_status_code_check(self.url, self.client.get, 200)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json()['results'][0]['pk'], self.project1.company.pk)

    def test_status_forbidden(self):
        for user in self.user_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_api_token_forbidden(self):
        for user in self.user_forbidden:
            self.api_token_check(user, 'scope_companies', self.url, self.client.get, 403, 403, 403)


class CompanyUpdateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:company-detail", pk=self.project1.company.pk)
        self.data = {"street": "randomstreet 1"}
        self.users_allowed = [
            self.management2, self.management1, self.customer1, self.pentester1, self.read_only1,
            self.pentester2
        ]
        self.users_forbidden = [
            self.user1
        ]

    def test_status_allowed(self):
        for user in self.users_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)

    def test_api_token_allowed(self):
        for user in self.users_allowed:
            self.api_token_check(user, 'scope_companies', self.url, self.client.patch, 403, 200, 403, data=self.data)

    def test_status_forbidden(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)

    def test_api_token_forbidden(self):
        for user in self.users_forbidden:
            self.api_token_check(user, 'scope_companies', self.url, self.client.patch, 403, 403, 403, data=self.data)

    def test_customer_forbidden_fields(self):
        self.client.force_login(self.customer1)
        self.data = {'report_template': "bla"}
        response = self.client.patch(self.url, self.data)
        self.assertEqual(response.json()['report_template'], self.customer1.company.report_template)

    def test_customer_status_notfound(self):
        self.client.force_login(self.customer2)
        self.basic_status_code_check(self.url, self.client.get, 404)

    def test_api_token_notfound(self):
        self.api_token_check(self.customer2, 'scope_companies', self.url, self.client.patch, 403, 404, 403,
                             data=self.data)


class CompanyCreateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:company-list")
        self.data = {"name": "test", "city": "asdf", "zipcode": "1234", "street": "teststreet",
                     "report_template": "default_template", "country": "asd"}
        self.users_allowed = [
            self.management2, self.management1
        ]
        self.users_forbidden = [
            self.user1, self.pentester2, self.pentester1, self.read_only1,
            self.customer2, self.customer1
        ]

    def test_status_forbidden(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)

    def test_status_allowed(self):
        for user in self.users_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)


class CompanyDestroyViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.company = self.create_instance(Company)
        self.url = self.get_url("api:backend:company-detail", pk=self.company.pk)

    def test_management_1(self):
        self.client.force_login(self.management1)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)

    def test_forbidden(self):
        users = [
            self.customer2, self.customer1, self.read_only1,
            self.pentester1, self.pentester2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)


class CompanyRetrieveViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:company-detail", pk=self.project1.company.pk)
        self.users_allowed = [
            self.management2, self.management1, self.pentester2, self.pentester1, self.read_only1,
            self.customer1
        ]
        self.users_forbidden = [
            self.user1
        ]

    def test_status_allowed(self):
        for user in self.users_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_status_forbidden(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_status_notfound(self):
        self.client.force_login(self.customer2)
        self.basic_status_code_check(self.url, self.client.get, 404)
