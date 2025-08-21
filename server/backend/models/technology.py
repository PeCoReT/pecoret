from django.db import models
from pecoret.core.models import TimestampedModel


class TechnologyQuerySet(models.QuerySet):
    def with_source_code(self, value: bool):
        if value is True:
            return self.filter(source_code_url__isnull=False)
        elif value is False:
            return self.filter(source_code_url__isnull=True)
        return self.all()


class Technology(TimestampedModel):
    objects = TechnologyQuerySet.as_manager()
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(null=True, blank=True)
    cpe = models.CharField(max_length=256, null=True)
    homepage = models.URLField(null=True, blank=True)
    vendor = models.CharField(max_length=256, null=True)
    source_code_url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ["name", "-date_updated"]

    def __str__(self):
        if self.cpe:
            return self.cpe
        return self.name

    @property
    def source_code_available(self):
        if self.source_code_url:
            return True
        return False
