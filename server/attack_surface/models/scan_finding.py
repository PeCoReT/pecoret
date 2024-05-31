from django.db import models

from backend.models.finding import Severity
from pecoret.core.models import TimestampedModel


class ScanFindingStatus(models.IntegerChoices):
    OPEN = 0, 'Open'
    CLOSED = 2, 'Closed'


class ScanFindingQuerySet(models.QuerySet):
    def for_program(self, program):
        return self.filter(program=program)

    def filter_unique(self, program, name, component, severity):
        return self.for_program(program).filter(name=name, affected_component=component,
                                                severity=Severity[severity.upper()].value)


class ScanFinding(TimestampedModel):
    objects = ScanFindingQuerySet.as_manager()
    tool = models.CharField(max_length=128)
    name = models.CharField(max_length=512)
    program = models.ForeignKey('attack_surface.Program', on_delete=models.CASCADE)
    affected_component = models.CharField(max_length=1024)
    result = models.TextField()
    full_output = models.TextField(blank=True, null=True)
    false_positive = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    severity = models.PositiveSmallIntegerField(choices=Severity.choices)
    status = models.PositiveSmallIntegerField(choices=ScanFindingStatus.choices, default=ScanFindingStatus.OPEN)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.program.save()

    class Meta:
        ordering = ['-date_created', '-severity']
