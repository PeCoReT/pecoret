from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models import Company, ReportTemplate


class CompanyListViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:company-list")

    def test_status_allowed(self):
        users = [
            self.management2, self.management1, self.read_only1, self.pentester2, self.pentester1,
            self.customer1, self.customer2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_customer(self):
        self.client.force_login(self.customer1)
        response = self.basic_status_code_check(self.url, self.client.get, 200)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json()['results'][0]['pk'], self.project1.company.pk)

    def test_status_forbidden(self):
        users = [
            self.user1, self.vendor1, self.vendor2, self.advisory_manager1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class CompanyUpdateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:company-detail", pk=self.project1.company.pk)
        self.data = {"street": "randomstreet 1"}

    def test_status_allowed(self):
        users = [
            self.management2, self.management1, self.customer1, self.pentester1, self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)

    def test_status_forbidden(self):
        users = [
            self.user1, self.pentester2, self.vendor2, self.vendor1,
            self.advisory_manager1, self.customer2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)

    def test_customer_forbidden_fields(self):
        self.client.force_login(self.customer1)
        self.report_template = self.create_instance(ReportTemplate)
        self.data = {'report_template': self.report_template.pk}
        response = self.client.patch(self.url, self.data)
        self.assertEqual(response.json()['report_template']['pk'], self.customer1.company.report_template.pk)


class CompanyCreateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:company-list")
        template = self.create_instance(ReportTemplate)
        self.data = {"name": "test", "city": "asdf", "zipcode": "1234", "street": "teststreet",
                     "report_template": template.pk, "country": "asd"}

    def test_status_forbidden(self):
        users = [
            self.user1, self.pentester2, self.pentester1, self.read_only1, self.vendor2, self.vendor1,
            self.customer2, self.customer1, self.advisory_manager1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)

    def test_status_allowed(self):
        users = [
            self.management2, self.management1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)


class CompanyDestroyViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.company = self.create_instance(Company)
        self.url = self.get_url("backend:company-detail", pk=self.company.pk)

    def test_management_1(self):
        self.client.force_login(self.management1)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)

    def test_forbidden(self):
        users = [
            self.customer2, self.customer1, self.advisory_manager1,
            self.vendor1, self.vendor2, self.read_only_vendor, self.read_only1,
            self.pentester1, self.pentester2
        ]


class CompanyRetrieveViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:company-detail", pk=self.project1.company.pk)

    def test_status_allowed(self):
        users = [
            self.management2, self.management1, self.pentester1, self.read_only1, self.customer1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_status_forbidden(self):
        users = [
            self.user1, self.advisory_manager1, self.vendor1, self.vendor2, self.pentester2,
            self.customer2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class APITokenReadTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.token1, self.key1 = self.create_api_token(self.pentester1, scope_companies=self.api_access_choices.READ,
                                                       date_expire=None)
        self.token2, self.key2 = self.create_api_token(self.pentester1,
                                                       scope_companies=self.api_access_choices.NO_ACCESS,
                                                       date_expire=None)
        self.token3, self.key3 = self.create_api_token(self.advisory_manager1,
                                                       scope_companies=self.api_access_choices.READ,
                                                       date_expire=None)
        self.url = self.get_url("backend:company-detail", pk=self.project1.company.pk)

    def test_valid(self):
        self.set_token_header(self.key1)
        self.basic_status_code_check(self.url, self.client.get, 200)

    def test_no_access_token(self):
        self.set_token_header(self.key2)
        self.basic_status_code_check(self.url, self.client.get, 403)

    def test_forbidden_user(self):
        self.set_token_header(self.key3)
        self.basic_status_code_check(self.url, self.client.get, 403)


class APITokenWriteTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.token1, self.key1 = self.create_api_token(self.pentester1, scope_companies=self.api_access_choices.READ,
                                                       date_expire=None)
        self.token2, self.key2 = self.create_api_token(self.pentester1,
                                                       scope_companies=self.api_access_choices.NO_ACCESS,
                                                       date_expire=None)
        self.token3, self.key3 = self.create_api_token(self.advisory_manager1,
                                                       scope_companies=self.api_access_choices.READ,
                                                       date_expire=None)
        self.url = self.get_url("backend:company-detail",
                                pk=self.project1.company.pk)
        self.data = {"name": "test123"}

    def test_valid(self):
        self.set_token_header(self.key1)
        self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)

    def test_read_write(self):
        self.token1.scope_companies = self.api_access_choices.READ_WRITE
        self.token1.save()
        self.set_token_header(self.key1)
        self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)

    def test_invalid(self):
        self.set_token_header(self.key2)
        self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)

    def test_forbidden(self):
        self.set_token_header(self.key3)
        self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)
