from django.conf import settings
from django.db import models
from django.utils.module_loading import import_string
from rest_framework.exceptions import ValidationError

from pecoret.core.permissions.group import Groups
from pecoret.core.models import TimestampedModel


class WebhookProvider(models.TextChoices):
    MATRIX = 'matrix', 'Matrix.org'
    GENERIC = 'generic', 'Generic'


class WebhookQuerySet(models.QuerySet):
    def for_event(self, event):
        return self.filter(**{f'event_{event.name}': True})

    def for_user(self, user):
        return self.filter(user=user)


# define groups for event fields. this prevents information leaks when
# e.g. a customer tries to create a webhook to receive target information
EVENT_FIELDS = {
    'event_new_target': [
        Groups.GROUP_PENTESTER
    ],
    'event_critical_scan_finding': [
        Groups.GROUP_PENTESTER
    ]
}


class Webhook(TimestampedModel):
    objects = WebhookQuerySet.as_manager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    secret = models.CharField(max_length=518, blank=True, null=True)
    url = models.URLField()
    # you can use this to define additional data
    additional_data = models.JSONField(blank=True, null=True)
    provider = models.CharField(max_length=128, choices=WebhookProvider.choices)

    # events, REMEMBER: add it to `EVENT_FIELDS` for validation!!!
    event_new_target = models.BooleanField(default=False, help_text='New Target created in Attack Surface application.')
    event_critical_scan_finding = models.BooleanField(default=False, help_text='New critical Scan Finding in Attack Surface application.')

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f'{self.pk} {self.provider} for {self.user}'

    def get_provider(self):
        # `self.provider` is a choice field so we can safely import it dynamically here
        provider_class = import_string(f'core.webhooks.providers.{self.provider}.WebhookProvider')
        return provider_class(self)

    def clean(self):
        # TODO: prevent type from being changed.
        for key in EVENT_FIELDS.keys():
            field = EVENT_FIELDS[key]
            if getattr(self, key) is True and not self.user.groups.filter(name__in=field).exists():
                raise ValidationError({key: 'you do not have permissions to receive webhooks for this event type.'})
        return super().clean()

    def patch_event_fields(self, group_names):
        # set event fields to false, when a user is no longer part of a group
        for key in EVENT_FIELDS.keys():
            field = EVENT_FIELDS[key]
            for group in field:
                if getattr(self, key) is True and group in list(group_names):
                    setattr(self, key, False)
        self.save()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
