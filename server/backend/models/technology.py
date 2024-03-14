from django.db import models
from pecoret.core.models import TimestampedModel


class Technology(TimestampedModel):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(null=True, blank=True)
    cpe = models.CharField(max_length=256, null=True, blank=True)
    homepage = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['name', '-date_updated']
