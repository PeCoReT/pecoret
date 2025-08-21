from django.contrib.auth.models import Group
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from backend.models import User
from core.webhooks.models import Webhook
from django.db.models.signals import post_migrate

DEFAULT_GROUPS = ['Admin', 'Pentester', 'Management', 'Customer']


@receiver(m2m_changed, sender=User.groups.through)
def user_group_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    """
    Signal handler to check if a user's group assignment changes.
    """
    if action in ["post_remove", "post_clear"] and pk_set:
        group_names = Group.objects.filter(pk__in=pk_set).values_list('name', flat=True)

        # user was removed from group
        webhooks = Webhook.objects.for_user(instance)
        for w in webhooks:
            w.patch_event_fields(group_names)



@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    for group_name in DEFAULT_GROUPS:
        Group.objects.get_or_create(name=group_name)
