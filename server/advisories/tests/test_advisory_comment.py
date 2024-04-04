from rest_framework.test import APITestCase
from advisories.models import AdvisoryComment
from pecoret.core.test import PeCoReTTestCaseMixin


class AdvisoryCommentCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.data = {"comment": "test"}
        self.url = self.get_url(
            "advisories:comment-list", advisory=self.advisory1.pk
        )

    def test_allowed(self):
        users = [self.advisory_manager1, self.pentester1, self.vendor1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 201, data=self.data
            )

    def test_forbidden(self):
        users = [
            self.pentester2,
            self.management1,
            self.management2,
            self.vendor2,
            self.read_only_vendor,
            self.read_only1,
            self.user1,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 403, data=self.data
            )


class AdvisoryCommentUpdateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.comment1 = self.create_instance(
            AdvisoryComment, advisory=self.advisory1, user=self.pentester1
        )
        self.url = self.get_url(
            "advisories:comment-detail",
            advisory=self.advisory1.pk,
            pk=self.comment1.pk,
        )
        self.data = {"comment": "new123"}

    def test_allowed(self):
        self.client.force_login(self.pentester1)
        response = self.basic_status_code_check(
            self.url, self.client.patch, 200, data=self.data
        )
        self.assertEqual(response.json()["comment"], self.data["comment"])

    def test_forbidden(self):
        users = [
            self.pentester2,
            self.vendor2,
            self.management1,
            self.management2,
            self.user1,
            self.read_only1,
            self.read_only_vendor
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 403)

    def test_not_found(self):
        users = [self.advisory_manager1, self.vendor1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 404)


class APITokenReadTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.token1, self.key1 = self.create_api_token(self.pentester1, scope_advisories=self.api_access_choices.READ,
                                                       date_expire=None)
        self.token2, self.key2 = self.create_api_token(self.pentester1,
                                                       scope_advisories=self.api_access_choices.NO_ACCESS,
                                                       date_expire=None)
        self.token3, self.key3 = self.create_api_token(self.pentester2,
                                                       scope_advisories=self.api_access_choices.READ,
                                                       date_expire=None)
        self.comment1 = self.create_instance(
            AdvisoryComment, advisory=self.advisory1, user=self.pentester1
        )
        self.url = self.get_url(
            "advisories:comment-detail",
            advisory=self.advisory1.pk,
            pk=self.comment1.pk,
        )

    def test_valid(self):
        self.set_token_header(self.key1)
        self.basic_status_code_check(self.url, self.client.get, 200)

    def test_invalid(self):
        self.set_token_header(self.key2)
        self.basic_status_code_check(self.url, self.client.get, 403)

    def test_forbidden(self):
        self.set_token_header(self.key3)
        self.basic_status_code_check(self.url, self.client.get, 403)


class APITokenWriteTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.token1, self.key1 = self.create_api_token(self.pentester1, scope_advisories=self.api_access_choices.READ,
                                                       date_expire=None)
        self.token2, self.key2 = self.create_api_token(self.pentester1,
                                                       scope_advisories=self.api_access_choices.NO_ACCESS,
                                                       date_expire=None)
        self.token3, self.key3 = self.create_api_token(self.pentester2,
                                                       scope_advisories=self.api_access_choices.READ,
                                                       date_expire=None)
        self.comment1 = self.create_instance(
            AdvisoryComment, advisory=self.advisory1, user=self.pentester1
        )
        self.url = self.get_url(
            "advisories:comment-detail",
            advisory=self.advisory1.pk,
            pk=self.comment1.pk,
        )
        self.data = {"comment": "test123"}

    def test_valid(self):
        self.set_token_header(self.key1)
        self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)

    def test_read_write(self):
        self.token1.scope_advisories = self.api_access_choices.READ_WRITE
        self.token1.save()
        self.set_token_header(self.key1)
        self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)

    def test_invalid(self):
        self.set_token_header(self.key2)
        self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)

    def test_forbidden(self):
        self.set_token_header(self.key3)
        self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)
