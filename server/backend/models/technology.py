from django.db import models
from pecoret.core.models import TimestampedModel


class Technology(TimestampedModel):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(null=True, blank=True)
    cpe = models.CharField(max_length=256, null=True, blank=True)
    homepage = models.URLField(null=True, blank=True)
    vendor = models.CharField(max_length=256, null=True, blank=True)
    source_code_url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['name', '-date_updated']

    @property
    def source_code_available(self):
        if self.source_code_url:
            return True
        return False
