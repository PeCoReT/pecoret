from django.utils import timezone
from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models.membership import Membership, Roles


class MembershipListViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:membership-list", project=self.project1.pk)
        self.users_allowed = [
            self.management1, self.pentester1, self.read_only1
        ]
        self.users_forbidden = [
            self.user1, self.pentester2, self.management2
        ]

    def test_status_code_allowed(self):
        for user in self.users_allowed:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_status_code_forbidden(self):
        for user in self.users_forbidden:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_api_token_forbidden(self):
        for user in self.users_forbidden:
            self.api_token_check(user, 'scope_all_projects', self.url, self.client.get, 403, 403, 403)


class MembershipCreateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:membership-list", project=self.project1.pk)
        self.data = {"user": self.pentester2.pk, "role": Roles.CONTRIBUTOR.label,
                     "active_until": timezone.now() + timezone.timedelta(days=3)}

    def test_status_code_allowed(self):
        for user in [self.management1]:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)
        qs = Membership.objects.filter(project=self.project1, user=self.pentester2)
        self.assertEqual(qs.count(), 1)

    def test_status_code_forbidden(self):
        users = [
            self.pentester2, self.pentester1, self.read_only1, self.user1,
            self.management2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)


class MembershipUpdateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.membership = Membership.objects.create(role=Roles.CONTRIBUTOR, project=self.project1,
                                                    user=self.pentester2,
                                                    active_until=timezone.now() + timezone.timedelta(days=3))
        self.url = self.get_url("api:backend:membership-detail", project=self.project1.pk, pk=self.membership.pk)
        self.data = {"active_until": timezone.now() + timezone.timedelta(days=300)}

    def test_status_code_allowed(self):
        for user in [self.management1]:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)

    def test_status_code_forbidden(self):
        users = [
            self.pentester2, self.pentester1, self.read_only1, self.management2,
            self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)


class MembershipMeViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()


class MembershipDestroyViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.membership = Membership.objects.create(role=Roles.CONTRIBUTOR, project=self.project1,
                                                    user=self.pentester2,
                                                    active_until=timezone.now() + timezone.timedelta(days=3))
        self.url = self.get_url("api:backend:membership-detail", project=self.project1.pk, pk=self.membership.pk)

    def test_status_code_allowed(self):
        for user in [self.management1]:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_status_code_forbidden(self):
        users = [
            self.management2, self.user1, self.pentester1, self.pentester2,
            self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)

    def test_last_owner_delete(self):
        self.client.force_login(self.management1)
        membership = Membership.objects.get(project=self.project1, user=self.management1)
        url = self.get_url("api:backend:membership-detail", project=self.project1.pk, pk=membership.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 400)
