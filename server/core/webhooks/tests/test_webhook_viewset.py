from rest_framework.test import APITestCase

from core.webhooks.models import Webhook
from pecoret.core.test import PeCoReTTestCaseMixin


class WebhookListView(PeCoReTTestCaseMixin, APITestCase):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('api:webhooks:webhook-list')
        self.allowed_users = [
            self.user1, self.pentester1, self.pentester2,
            self.management1, self.management2, self.read_only1,
            self.customer1, self.customer2,
        ]
        self.webhook = self.create_instance(Webhook, user=self.pentester1)

    def test_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_see_others(self):
        self.client.force_login(self.user1)
        response = self.basic_status_code_check(self.url, self.client.get, 200)
        self.assertEqual(response.data['count'], 0)
        self.client.force_login(self.pentester1)
        response = self.basic_status_code_check(self.url, self.client.get, 200)
        self.assertEqual(response.data['count'], 1)


class WebhookCreateView(PeCoReTTestCaseMixin, APITestCase):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url('api:webhooks:webhook-list')
        self.allowed_users = [
            self.user1, self.pentester1, self.pentester2,
            self.management1, self.management2, self.read_only1,
            self.customer1, self.customer2,
        ]
        self.data = {
            'secret': 'test',
            'url': 'http://localhost',
            'provider': 'matrix',
            'additional_data': {}
        }

    def test_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_field_permissions(self):
        self.client.force_login(self.user1)
        self.data['event_new_target'] = True
        self.basic_status_code_check(self.url, self.client.post, 400, data=self.data)
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)
        self.assertEqual(Webhook.objects.for_user(self.pentester1).get().event_new_target, True)