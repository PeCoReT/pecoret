from django.contrib.auth.models import Group
from rest_framework.test import APITestCase

from core.webhooks.models import Webhook
from pecoret.core.test import PeCoReTTestCaseMixin


class TestGroupChanges(PeCoReTTestCaseMixin, APITestCase):
    def setUp(self):
        self.init_mixin()
        self.webhook1 = self.create_instance(Webhook, user=self.pentester1, event_new_target=True)
        self.webhook2 = self.create_instance(Webhook, user=self.pentester2, event_new_target=True)

    def test_group_changes(self):
        self.pentester1.groups.remove(Group.objects.get(name='Pentester'))
        self.pentester1.save()
        self.assertEqual(Webhook.objects.for_user(self.pentester1).filter(event_new_target=True).count(), 0)
        self.assertEqual(Webhook.objects.for_user(self.pentester2).filter(event_new_target=True).count(), 1)
