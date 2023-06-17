from django.core.mail import outbox
from rest_framework.test import APITestCase
from pecoret.core.test import AdvisoryTestCaseMixin
from backend.models.advisory_membership import Roles


class AdvisoryMembershipCreateView(APITestCase, AdvisoryTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url(
            "backend:advisories:membership-list", advisory=self.advisory1.pk
        )
        self.data = {
            "email": self.management1.email,
            "role": Roles.READ_ONLY.label,
            "active_until": "2099-10-10",
        }

    def test_allowed(self):
        self.client.force_login(self.advisory_manager1)
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)
        # TODO: fix github action with django-q2
        # self.assertEqual(len(outbox), 0)

    def test_forbidden(self):
        users = [
            self.pentester2,
            self.pentester1,
            self.read_only1,
            self.management1,
            self.management2,
            self.user1,
            self.vendor1,
            self.vendor2,
            self.read_only_vendor,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 403, data=self.data
            )

    def test_draft_forbidden(self):
        self.url = self.get_url(
            "backend:advisories:membership-list", advisory=self.advisory2.pk
        )
        users = [
            self.pentester1,
            self.read_only1,
            self.management2,
            self.management1,
            self.user1,
            self.vendor2,
            self.vendor1,
            self.advisory_manager1,
            self.pentester2,
            self.read_only_vendor,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 403, data=self.data
            )


class AdvisoryMembershipListView(APITestCase, AdvisoryTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.membership2 = self.assign_advisory_role(
            self.vendor2, Roles.READ_ONLY, self.advisory2
        )
        self.url = self.get_url(
            "backend:advisories:membership-list", advisory=self.advisory1.pk
        )

    def test_advisory_management(self):
        self.client.force_login(self.advisory_manager1)
        response = self.basic_status_code_check(self.url, self.client.get, 200)
        self.assertEqual(response.json()["count"], 3)

    def test_allowed(self):
        users = [self.pentester1, self.vendor1, self.read_only_vendor]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [
            self.vendor2,
            self.management1,
            self.management2,
            self.pentester2,
            self.user1,
            self.read_only1,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_draft_allowed(self):
        self.url = self.get_url(
            "backend:advisories:membership-list", advisory=self.advisory2.pk
        )
        users = [self.pentester2]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_draft_forbidden(self):
        self.url = self.get_url(
            "backend:advisories:membership-list", advisory=self.advisory2.pk
        )
        users = [
            self.vendor1,
            self.vendor2,
            self.management2,
            self.management1,
            self.pentester1,
            self.user1,
            self.read_only1,
            self.advisory_manager1,
            self.read_only_vendor,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class AdvisoryMembershipUpdateView(APITestCase, AdvisoryTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()


class AdvisoryMembershipDestroyView(APITestCase, AdvisoryTestCaseMixin):
    """test if the membership destroy view is handled correctly
    we should check, if the advisory_manager is the only one allowed to delete memberships
    """

    def setUp(self) -> None:
        self.init_mixin()
        self.membership = self.assign_advisory_role(
            self.vendor2, Roles.READ_ONLY, self.advisory1
        )
        self.membership2 = self.assign_advisory_role(
            self.vendor1, Roles.READ_ONLY, self.advisory2
        )
        self.url = self.get_url(
            "backend:advisories:membership-detail",
            advisory=self.advisory1.pk,
            pk=self.membership.pk,
        )

    def test_allowed(self):
        self.client.force_login(self.advisory_manager1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_forbidden(self):
        users = [
            self.pentester2,
            self.pentester1,
            self.vendor2,
            self.vendor1,
            self.user1,
            self.read_only1,
            self.management2,
            self.management1,
            self.read_only_vendor,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)

    def test_draft_forbidden(self):
        self.url = self.get_url(
            "backend:advisories:membership-detail",
            advisory=self.advisory2.pk,
            pk=self.membership2.pk,
        )
        users = [
            self.pentester2,
            self.pentester1,
            self.vendor2,
            self.vendor1,
            self.user1,
            self.read_only1,
            self.management1,
            self.management2,
            self.advisory_manager1,
            self.read_only_vendor,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)
