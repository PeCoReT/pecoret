from datetime import timedelta

from django.apps import apps
from django.db import models
from django.db.models import Count
from django.utils import timezone

from pecoret.core.models import TimestampedModel


class InputTypeChoices(models.TextChoices):
    SERVICES = 'services'
    TARGETS = 'targets'
    URLS = 'urls'
    PROGRAMS = 'programs'

    @classmethod
    def get_related_item_class(cls, value):
        """Return the related name for the given field value."""
        if value == cls.TARGETS:
            return apps.get_model(f'attack_surface.target')
        elif value == cls.SERVICES:
            return apps.get_model(f'attack_surface.service')
        elif value == cls.URLS:
            return apps.get_model(f'attack_surface.url')
        elif value == cls.PROGRAMS:
            return apps.get_model(f'attack_surface.program')
        return None


class PriorityChoices(models.IntegerChoices):
    MANUAL = 1, "manual"
    EVENT = 2, "event"
    SCHEDULED = 3, "scheduled"


class ScanTemplateQueryset(models.QuerySet):
    def enabled(self):
        return self.filter(enabled=True)

    def rate_limit_checked(self):
        # Define the start of the 24-hour window for rate limiting
        rate_limit_period_start = timezone.now() - timedelta(days=1)
        annotated = self.annotate(scan_count=Count('scanbatchrequest', filter=models.Q(
            scanbatchrequest__date_created__gt=rate_limit_period_start)))
        return annotated.exclude(scan_count__gte=models.F('rate_limit'))


class ScanTemplate(TimestampedModel):
    InputTypes = InputTypeChoices
    objects = ScanTemplateQueryset.as_manager()

    name = models.CharField(
        max_length=100,
        help_text="Human-readable name for the scan template (e.g., External ASN Lookup)"
    )
    scan_type = models.CharField(max_length=50, help_text="Type of scan being performed")
    input_type = models.CharField(max_length=32, choices=InputTypeChoices.choices,
                                  help_text="Type of object this scan runs on (Target, Service, or URL)"
                                  )
    priority = models.PositiveIntegerField(choices=PriorityChoices.choices, default=PriorityChoices.MANUAL,
                                           help_text="Scan dispatch priority: manual > event > scheduler"
                                           )

    cooldown = models.DurationField(
        help_text="Minimum interval before the same object can be scanned again with this template (e.g., 3 days)"
    )
    rate_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Optional: max number of scans allowed for this template per 24h window"
    )
    batch_threshold = models.PositiveIntegerField(
        default=10,
        help_text="Minimum number of input items required to trigger a batch"
    )
    trickle_delay = models.DurationField(
        null=True,
        blank=True,
        help_text="Optional: max delay before dispatching a scan even if batch threshold is not met"
    )
    is_discovery_scan = models.BooleanField(
        default=False,
        help_text="Set True if this scan may discover new assets (will enforce single-program batches)"
    )

    enabled = models.BooleanField(
        default=True,
        help_text="Controls whether this scan template is active and eligible for dispatch"
    )
    description = models.TextField(
        blank=True,
        help_text="Optional longer description of what the scan does or when it is used"
    )
    scanner_config = models.JSONField(default=dict, blank=True, help_text="Optional scanner config")
    conditions = models.TextField(blank=True, null=True, help_text="Optional django-q2 filters")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Scan Templates'
