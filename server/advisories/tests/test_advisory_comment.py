from rest_framework.test import APITestCase

from advisories.models import AdvisoryComment
from pecoret.core.test import PeCoReTTestCaseMixin


class AdvisoryCommentCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.data = {"comment": "test"}
        self.url = self.get_url(
            "api:advisories:comment-list", advisory=self.advisory1.pk
        )
        self.allowed_users = [self.pentester1, self.pentester2, self.read_only1]
        self.forbidden_users = [self.management1, self.management2, self.user1]

    def test_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 201, data=self.data
            )

    def test_forbidden(self):

        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 403, data=self.data
            )

    def test_api_token_allowed(self):
        for user in self.allowed_users:
            self.api_token_check(user, 'scope_advisories', self.url, self.client.post,
                                 403, 201, 403, data=self.data)

    def test_api_token_forbidden(self):
        for user in self.forbidden_users:
            self.api_token_check(user, 'scope_advisories', self.url, self.client.post, 403, 403, 403)


class AdvisoryCommentUpdateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.comment1 = self.create_instance(
            AdvisoryComment, advisory=self.advisory1, user=self.pentester1
        )
        self.comment2 = self.create_instance(
            AdvisoryComment, advisory=self.advisory2, user=self.pentester2
        )
        self.url = self.get_url(
            "api:advisories:comment-detail",
            advisory=self.advisory1.pk,
            pk=self.comment1.pk,
        )
        self.url2 = self.get_url(
            'api:advisories:comment-detail', advisory=self.advisory2.pk, pk=self.comment1.pk
        )
        self.data = {"comment": "new123"}
        self.forbidden_users = [self.management1, self.management2, self.user1, self.customer2, self.customer1]

    def test_allowed(self):
        self.client.force_login(self.pentester1)
        response = self.basic_status_code_check(
            self.url, self.client.patch, 200, data=self.data
        )
        self.assertEqual(response.json()["comment"], self.data["comment"])

    def test_broken_access(self):
        self.client.force_login(self.pentester2)
        self.basic_status_code_check(self.url, self.client.patch, 404, data=self.data)
        self.client.force_login(self.read_only1)
        self.basic_status_code_check(self.url, self.client.patch, 404, data=self.data)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 403)

    def test_api_token_allowed(self):
        self.api_token_check(self.pentester1, 'scope_advisories', self.url, self.client.patch, 403, 200, 403,
                             data=self.data)

    def test_api_token_forbidden(self):
        for user in self.forbidden_users:
            self.api_token_check(user, 'scope_advisories', self.url, self.client.patch, 403, 403, 403, data=self.data)
        # test IDOR
        self.api_token_check(self.pentester2, 'scope_advisories', self.url2, self.client.patch, 403, 404, 403,
                             data=self.data)

    def test_api_token_not_found(self):
        for user in [self.pentester2]:
            self.api_token_check(user, 'scope_advisories', self.url, self.client.patch, 403, 404, 403, data=self.data)


class AdvisoryCommentRetrieveView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.comment1 = self.create_instance(
            AdvisoryComment, advisory=self.advisory1, user=self.pentester1
        )
        self.url = self.get_url(
            "api:advisories:comment-detail",
            advisory=self.advisory1.pk,
            pk=self.comment1.pk,
        )
        self.allowed_users = [self.pentester1, self.pentester2, self.read_only1]
        self.forbidden_users = [self.customer2, self.customer1, self.management2, self.management1, self.user1]

    def test_api_token_allowed(self):
        for user in self.allowed_users:
            self.api_token_check(user, 'scope_advisories', self.url, self.client.get, 200, 200, 403)

    def test_api_token_forbidden(self):
        for user in self.forbidden_users:
            self.api_token_check(user, 'scope_advisories', self.url, self.client.get, 403, 403, 403)
