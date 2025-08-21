from django.core.validators import RegexValidator
from django.db import models

from pecoret.core.models import TimestampedModel


class ScanRuleQuerySet(models.QuerySet):
    def with_event_type(self, event_type):
        return self.filter(event_type=event_type)


class ScanRule(TimestampedModel):
    objects = ScanRuleQuerySet.as_manager()
    event_type = models.CharField(max_length=32, validators=[RegexValidator(regex=r'^[a-z0-9-.:]+$')])
    description = models.TextField(blank=True, null=True)
    scan_templates = models.ManyToManyField('ScanTemplate', blank=True)

    def __str__(self):
        return f"Rule for {self.event_type}"

    class Meta:
        ordering = ['-date_created']
        verbose_name_plural = 'Scan Rules'
