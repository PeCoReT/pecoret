from rest_framework.test import APITestCase
from backend.models.finding_timeline import FindingTimeline
from pecoret.core.test import PeCoReTTestCaseMixin


class FindingTimelineListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.timeline1 = self.create_instance(
            FindingTimeline,
            finding__user=self.pentester1,
            finding__vulnerability__project=self.project1,
            finding__component=self.asset1,
            finding__component_object_id=self.asset1.pk,
            finding__component_content_type=self.get_content_type_for_model(self.asset1.__class__),
            finding__project=self.project1,
        )
        self.timeline2 = self.create_instance(
            FindingTimeline,
            finding__user=self.pentester2,
            finding__vulnerability__project=self.project2,
            finding__component=self.asset2,
            finding__component_object_id=self.asset2.pk,
            finding__component_content_type=self.get_content_type_for_model(self.asset2.__class__),
            finding__project=self.project2,
        )
        self.url = self.get_url(
            "backend:findings:timeline-list",
            project=self.project1.pk,
            finding=self.timeline1.finding.pk,
        )
        self.users_allowed = [
            self.read_only1, self.pentester1, self.management1
        ]
        self.users_forbidden = [
            self.management2, self.advisory_manager1, self.pentester2, self.user1
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
            self.api_token_check(user, 'scope_all_projects', self.url, self.client.get, 200, 200, 403)

    def test_api_token_forbidden(self):
        for user in self.users_forbidden:
            self.api_token_check(user, 'scope_all_projects', self.url, self.client.get, 403, 403, 403)

    def test_broken_access(self):
        self.url = self.get_url(
            "backend:findings:timeline-list",
            project=self.project1.pk,
            finding=self.timeline2.finding.pk,
        )
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.get, 403)
