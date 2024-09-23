import uuid
from django.dispatch import receiver
from django.db import models

from rest_framework.exceptions import ValidationError

from attack_surface.queue import enqueue_scan
from pecoret.core.models import TimestampedModel


class ScanStatus(models.IntegerChoices):
    PENDING = 0, 'Pending'
    RUNNING = 1, 'Running'
    COMPLETED = 2, 'Completed'
    FAILED = 3, 'Failed'


class Scan(TimestampedModel):
    scan_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scan_type = models.ForeignKey('attack_surface.ScanType', on_delete=models.PROTECT)
    status = models.PositiveSmallIntegerField(choices=ScanStatus.choices, default=ScanStatus.PENDING)
    output = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    job_id = models.CharField(max_length=255, null=True, blank=True, help_text="Job ID received from rq")

    def delete(self, using=None, keep_parents=False):
        if self.status == ScanStatus.PENDING.value:
            return super().delete(using, keep_parents)
        raise ValidationError({'status': 'Only scans with status "pending" can be deleted.'})
