import secrets

from django.conf import settings
from django.db import models
from django.utils import timezone

from pecoret.core.models import TimestampedModel


def generate_token():
    return secrets.token_urlsafe(132).replace("_", "-")


class ShareTokenQuerySet(models.QuerySet):
    def for_advisory(self, advisory):
        return self.filter(advisory=advisory)


class ShareToken(TimestampedModel):
    objects = ShareTokenQuerySet.as_manager()
    name = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True, default=generate_token)
    advisory = models.ForeignKey('advisories.Advisory', on_delete=models.CASCADE)
    date_expire = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date_created']
        unique_together = [('name', 'advisory')]

    def is_expired(self):
        if not self.date_expire:
            return False
        return timezone.now() >= self.date_expire

    @property
    def url(self):
        base_url = settings.SITE_URL
        path = settings.SITE_URLS.get("ADVISORY_SHARE_TOKEN_DOWNLOAD").format(advisoryId=self.advisory.pk,
                                                                              token=self.token)
        return f'{base_url}{path}'
