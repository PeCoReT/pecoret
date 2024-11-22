from django.dispatch import receiver
from django.db import models
from pecoret.core.models import PeCoReTBaseModel
from .user import User


class UserSettingsQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user=user)


class UserSettings(PeCoReTBaseModel):
    """stores the settings of a user
    """
    objects = UserSettingsQuerySet.as_manager()
    user = models.OneToOneField('backend.User', on_delete=models.CASCADE)

    # advisories
    # send notification mails, when disclosure of advisory is soon
    notify_before_disclosure_mail = models.BooleanField(default=False)

    # notifications
    notify_critical_findings = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


@receiver(models.signals.post_save, sender=User)
def create_user_settings_object(sender, instance, created, **kwargs):
    """creates a new `UserSetting` when a new user is created

    Args:
        sender (_type_): _description_
        instance (_type_): _description_
        created (_type_): _description_
    """
    if created:
        UserSettings.objects.create(user=instance)
