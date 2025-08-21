import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from pecoret.core.models import TimestampedModel
from .scan_template import ScanTemplate


class StatusChoices(models.IntegerChoices):
    PENDING = 0, "Pending"
    IN_PROGRESS = 1, "In Progress"
    COMPLETED = 2, "Completed"
    FAILED = 3, "Failed"
    REQUEUED = 4, "Requeued"
    STAGING = 5, "Staging"


class TriggerSource(models.IntegerChoices):
    MANUAL = 0, "Manual"
    SCHEDULED = 1, "Scheduled"
    EVENT = 2, "Event"
    CONTINUOUS = 3, "Continuous"


class ScanBatchQuerySet(models.QuerySet):
    def with_status(self, status):
        return self.filter(status=status)

    def with_status_staging(self):
        return self.filter(status=StatusChoices.STAGING)

    def with_status_pending(self):
        return self.filter(status=StatusChoices.PENDING)

    def with_template(self, template):
        return self.filter(scan_template=template)


class ScanBatchRequest(TimestampedModel):
    objects = ScanBatchQuerySet.as_manager()

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    scan_template = models.ForeignKey(ScanTemplate, on_delete=models.CASCADE)
    targets = models.ManyToManyField('attack_surface.Target', related_name='scan_batches', blank=True)
    services = models.ManyToManyField('attack_surface.Service', related_name='scan_batches', blank=True)
    urls = models.ManyToManyField('attack_surface.URL', related_name='scan_batches', blank=True)
    programs = models.ManyToManyField('attack_surface.Program', related_name='scan_batches', blank=True)

    # Scanning metadata, is queried a lot to determine old scan targets, so db index = true
    status = models.PositiveSmallIntegerField(choices=StatusChoices.choices, default=StatusChoices.STAGING,
                                              db_index=True)
    batch_start_time = models.DateTimeField(null=True, blank=True, db_index=True)
    batch_end_time = models.DateTimeField(null=True, blank=True, db_index=True)

    # Admin or system user who triggered the batch
    triggered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    scan_trigger_source = models.PositiveSmallIntegerField(choices=TriggerSource.choices, default=TriggerSource.MANUAL)

    # Additional fields for business logic (e.g., discovery)
    is_discovery_scan = models.BooleanField(default=False)

    date_last_item_added = models.DateTimeField(null=True, blank=True)

    # Optional custom notes for the batch
    notes = models.TextField(null=True, blank=True)

    # TODO: move to separate model so we can have a scan result history
    raw_output = models.TextField(null=True, blank=True)
    errors = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Scan Batch {self.pk} - {self.scan_template}"

    def get_item_field(self):
        return getattr(self, self.scan_template.input_type, None)

    def add_items(self, new_items):
        field = self.get_item_field()
        field.add(*new_items)
        self.date_last_item_added = timezone.now()
        self.save()

    def mark_full(self):
        self.status = StatusChoices.PENDING
        self.save()

    class Meta:
        ordering = ['-date_created']
        verbose_name_plural = 'Scan Batch Requests'
