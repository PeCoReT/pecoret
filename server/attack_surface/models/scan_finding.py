from django.db import models
from django.dispatch import receiver
from django_q.tasks import async_task

from backend.models.finding import Severity
from core.webhooks.event import Event
from core.webhooks.models import Webhook
from pecoret.core.models import TimestampedModel


class ScanFindingStatus(models.IntegerChoices):
    OPEN = 0, 'Open'
    CLOSED = 2, 'Closed'


class ScanFindingQuerySet(models.QuerySet):

    def filter_unique(self, name, component, severity):
        return self.filter(name=name, affected_component=component,
                           severity=Severity[severity.upper()].value)


class ScanFinding(TimestampedModel):
    objects = ScanFindingQuerySet.as_manager()
    tool = models.CharField(max_length=128)
    name = models.CharField(max_length=512)
    affected_component = models.CharField(max_length=1024)
    result = models.TextField()
    full_output = models.TextField(blank=True, null=True)
    false_positive = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    severity = models.PositiveSmallIntegerField(choices=Severity.choices)
    status = models.PositiveSmallIntegerField(choices=ScanFindingStatus.choices, default=ScanFindingStatus.OPEN)
    ignore_until = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_created', '-severity']

    def __str__(self):
        return self.name

    def get_frontend_url(self):
        return f'/#/attack-surface/scan-findings/{self.pk}/'


@receiver(models.signals.post_save, sender=ScanFinding)
def webhook_new_critical_scan_finding(sender, instance, created, **kwargs):
    if created and instance.severity == Severity.CRITICAL:
        e = Event(
            'critical_scan_finding',
            'Scanner',
            'created new critical scan finding',
            action_object=instance,
            target=instance,
        )
        for w in Webhook.objects.for_event(e):
            async_task(w.get_provider().send, e)
