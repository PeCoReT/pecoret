from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from advisories.models.advisory_timeline import AdvisoryTimeline


class AdvisoryTimelineCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url(
            "advisories:timeline-list", advisory=self.advisory1.pk
        )
        self.data = {"text": "test", "date": "2022-01-01"}
        self.users_allowed = [self.advisory_manager1, self.pentester1]
        self.users_forbidden = [
            self.pentester2,
            self.management2,
            self.management1,
            self.read_only1,
            self.user1,
            self.vendor1,
            self.vendor2, self.read_only_vendor,
        ]

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

    def test_draft_forbidden(self):
        users = [
            self.management1,
            self.management2,
            self.user1,
            self.read_only1,
            self.advisory_manager1,
            self.vendor1,
            self.vendor2,
            self.pentester2,
            self.read_only_vendor,
        ]
        for user in users:
            self.client.force_login(user)


class AdvisoryTimelineDestroyView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.timeline1 = self.create_instance(AdvisoryTimeline, advisory=self.advisory1)
        self.timeline2 = self.create_instance(AdvisoryTimeline, advisory=self.advisory2)
        self.url = self.get_url(
            "advisories:timeline-detail",
            advisory=self.advisory1.pk,
            pk=self.timeline1.pk,
        )

    def test_advisory_management(self):
        self.client.force_login(self.advisory_manager1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_forbidden(self):
        users = [
            self.management1,
            self.management2,
            self.user1,
            self.read_only1,
            self.pentester2,
            self.vendor2,
            self.vendor1,
            self.read_only_vendor,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)

    def test_draft_allowed(self):
        self.url = self.get_url(
            "advisories:timeline-detail",
            advisory=self.advisory2.pk,
            pk=self.timeline2.pk,
        )
        users = [
            self.pentester2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_draft_forbidden(self):
        self.url = self.get_url(
            "advisories:timeline-detail",
            advisory=self.advisory2.pk,
            pk=self.timeline2.pk,
        )
        users = [
            self.user1,
            self.read_only1,
            self.vendor1,
            self.vendor2,
            self.management2,
            self.management1,
            self.pentester1,
            self.advisory_manager1,
            self.read_only_vendor,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)

    def test_broken_access(self):
        self.timeline2.is_draft = True
        self.timeline2.save()
        self.url = self.get_url(
            "advisories:timeline-detail",
            advisory=self.advisory1.pk,
            pk=self.timeline2.pk,
        )
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 404)


class AdvisoryTimelineUpdateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.timeline1 = self.create_instance(AdvisoryTimeline, advisory=self.advisory1)
        self.timeline2 = self.create_instance(AdvisoryTimeline, advisory=self.advisory2)
        self.url = self.get_url(
            "advisories:timeline-detail",
            advisory=self.advisory1.pk,
            pk=self.timeline1.pk,
        )
        self.data = {"text": "anothertest"}

    def test_allowed(self):
        users = [self.advisory_manager1, self.pentester1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.patch, 200, data=self.data
            )

    def test_draft_allowed(self):
        self.url = self.get_url(
            "advisories:timeline-detail",
            advisory=self.advisory2.pk,
            pk=self.timeline2.pk,
        )
        users = [self.pentester2]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.patch, 200, data=self.data
            )

    def test_forbidden(self):
        users = [
            self.user1,
            self.read_only1,
            self.management2,
            self.management1,
            self.pentester2,
            self.vendor2,
            self.vendor1,
            self.read_only_vendor,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.patch, 403, data=self.data
            )

    def test_broken_access(self):
        self.url = self.get_url(
            "advisories:timeline-detail",
            advisory=self.advisory1.pk,
            pk=self.timeline2.pk,
        )
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.patch, 404, data=self.data)
        self.client.force_login(self.advisory_manager1)
        self.basic_status_code_check(self.url, self.client.patch, 404, data=self.data)
        self.url = self.get_url(
            "advisories:timeline-detail",
            advisory=self.advisory2.pk,
            pk=self.timeline1.pk,
        )
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)

    def test_draft_forbidden(self):
        self.url = self.get_url(
            "advisories:timeline-detail",
            advisory=self.advisory2.pk,
            pk=self.timeline2.pk,
        )

        users = [
            self.pentester1,
            self.vendor2,
            self.vendor1,
            self.management1,
            self.management2,
            self.read_only1,
            self.advisory_manager1,
            self.read_only_vendor,
        ]
        for user in users:
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
            "advisories:timeline-list", advisory=self.advisory1.pk
        )
        self.allowed_users = [
            self.pentester1,
            self.vendor1,
            self.advisory_manager1,
            self.read_only_vendor,
        ]
        self.forbidden_users = [
            self.pentester2,
            self.management2,
            self.management1,
            self.read_only1,
            self.user1,
            self.vendor2,
        ]

    def test_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_draft_allowed(self):
        self.url = self.get_url(
            "advisories:timeline-list", advisory=self.advisory2.pk
        )
        users = [self.pentester2]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_api_token_forbidden(self):
        for user in self.forbidden_users:
            self.api_token_check(user, 'scope_advisories', self.url, self.client.get, 403, 403, 403)

    def test_draft_forbidden(self):
        self.url = self.get_url(
            "advisories:timeline-list", advisory=self.advisory2.pk
        )
        users = [
            self.advisory_manager1,
            self.pentester1,
            self.vendor1,
            self.vendor2,
            self.management1,
            self.management2,
            self.read_only1,
            self.user1,
            self.read_only_vendor,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)
