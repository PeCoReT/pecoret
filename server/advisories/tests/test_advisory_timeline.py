from rest_framework.test import APITestCase

from advisories.models.advisory_timeline import AdvisoryTimeline
from pecoret.core.test import PeCoReTTestCaseMixin


class AdvisoryTimelineCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url(
            "api:advisories:timeline-list", advisory=self.advisory1.pk
        )
        self.data = {"text": "test", "date": "2022-01-01"}
        self.users_allowed = [self.pentester2, self.pentester1, self.read_only1]
        self.users_forbidden = [self.management1, self.management2, self.user1]

    def test_allowed(self):
        for user in self.users_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 201, data=self.data
            )

    def test_api_token_allowed(self):
        for user in self.users_allowed:
            self.api_token_check(user, 'scope_advisories', self.url, self.client.post, 403, 201, 403, data=self.data)

    def test_forbidden(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 403, data=self.data
            )

    def test_api_token_forbidden(self):
        for user in self.users_forbidden:
            self.api_token_check(user, 'scope_advisories', self.url, self.client.post, 403, 403, 403, data=self.data)


class AdvisoryTimelineDestroyView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.timeline1 = self.create_instance(AdvisoryTimeline, advisory=self.advisory1)
        self.timeline2 = self.create_instance(AdvisoryTimeline, advisory=self.advisory2)
        self.url = self.get_url(
            "api:advisories:timeline-detail",
            advisory=self.advisory1.pk,
            pk=self.timeline1.pk,
        )
        self.forbidden_users = [self.management1, self.management2, self.user1]

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)


class AdvisoryTimelineUpdateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.timeline1 = self.create_instance(AdvisoryTimeline, advisory=self.advisory1)
        self.timeline2 = self.create_instance(AdvisoryTimeline, advisory=self.advisory2)
        self.url = self.get_url(
            "api:advisories:timeline-detail",
            advisory=self.advisory1.pk,
            pk=self.timeline1.pk,
        )
        self.data = {"text": "anothertest"}
        self.allowed_users = [self.pentester2, self.pentester1, self.read_only1]
        self.forbidden_users = [self.management1, self.management2, self.user1]

    def test_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.patch, 200, data=self.data
            )

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.patch, 403, data=self.data
            )


class AdvisoryTimelineListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.timeline1 = self.create_instance(AdvisoryTimeline, advisory=self.advisory1)
        self.timeline2 = self.create_instance(AdvisoryTimeline, advisory=self.advisory2)
        self.url = self.get_url(
            "api:advisories:timeline-list", advisory=self.advisory1.pk
        )
        self.allowed_users = [self.pentester1, self.pentester2, self.read_only1]
        self.forbidden_users = [self.management2, self.management1, self.user1]

    def test_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_api_token_forbidden(self):
        for user in self.forbidden_users:
            self.api_token_check(user, 'scope_advisories', self.url, self.client.get, 403, 403, 403)
