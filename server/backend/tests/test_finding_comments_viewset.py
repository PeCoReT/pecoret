from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models.finding_comment import FindingComment
from backend.models.finding import Finding


class FindingCommentListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.finding1 = self.create_finding(
            user=self.pentester1,
            vulnerability__project=self.project1,
            project=self.project1,
            component=self.asset1
        )
        self.comment1 = self.create_instance(
            FindingComment,
            finding=self.finding1
        )
        self.finding2 = self.create_finding(
            user=self.pentester2,
            vulnerability__project=self.project2,
            project=self.project2,
            component=self.asset2
        )

        self.comment2 = self.create_instance(
            FindingComment,
            finding=self.finding2
        )
        self.url = self.get_url(
            "backend:findings:comment-list",
            project=self.project1.pk,
            finding=self.comment1.finding.pk,
        )

    def test_allowed(self):
        users = [self.read_only1, self.pentester1, self.management1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [self.advisory_manager1, self.user1, self.management2, self.pentester2]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class FindingCommentCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.finding1 = self.create_finding(
            component=self.asset1,
            vulnerability__project=self.project1,
            project=self.project1,
            user=self.pentester1,
        )
        self.finding2 = self.create_finding(
            component=self.asset2,
            vulnerability__project=self.project2,
            project=self.project2,
            user=self.pentester2,
        )
        self.url = self.get_url(
            "backend:findings:comment-list",
            project=self.project1.pk,
            finding=self.finding1.pk,
        )
        self.data = {"comment": "test comment"}

    def test_allowed(self):
        users = [self.pentester1, self.management1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 201, data=self.data
            )

    def test_forbidden(self):
        users = [
            self.pentester2,
            self.management2,
            self.advisory_manager1,
            self.user1,
            self.read_only1,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 403, data=self.data
            )

    def test_broken_access(self):
        self.client.force_login(self.pentester1)
        self.url = self.get_url(
            "backend:findings:comment-list",
            project=self.project1.pk,
            finding=self.finding2.pk,
        )
        self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)


class FindingCommentDestroyView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.finding1 = self.create_finding(
            user=self.pentester1,
            vulnerability__project=self.project1,
            component=self.asset1,
            project=self.project1
        )
        self.comment1 = self.create_instance(
            FindingComment,
            finding=self.finding1
        )
        self.url = self.get_url(
            "backend:findings:comment-detail",
            project=self.project1.pk,
            finding=self.comment1.finding.pk,
            pk=self.comment1.pk,
        )

    def test_not_implemented(self):
        users = [self.management1, self.pentester1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 405)

    def test_forbidden(self):
        users = [
            self.pentester2,
            self.management2,
            self.advisory_manager1,
            self.read_only1,
            self.user1,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)


class FindingCommentUpdateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.finding1 = self.create_finding(
            component=self.asset1,
            vulnerability__project=self.project1,
            project=self.project1,
            user=self.pentester1,
        )
        self.finding2 = self.create_finding(
            component=self.asset2,
            vulnerability__project=self.project2,
            project=self.project2,
            user=self.pentester2,
        )
        self.comment1 = self.create_instance(FindingComment, finding=self.finding1)
        self.url = self.get_url(
            "backend:findings:comment-detail",
            project=self.project1.pk,
            finding=self.finding1.pk,
            pk=self.comment1.pk,
        )
        self.data = {"comment": "test comment"}

    def test_allowed(self):
        users = [self.pentester1, self.management1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.patch, 200, data=self.data
            )

    def test_forbidden(self):
        users = [self.pentester2, self.management2, self.read_only1, self.user1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.patch, 403, data=self.data
            )
