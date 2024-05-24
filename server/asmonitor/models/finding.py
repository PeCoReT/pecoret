from django.core.exceptions import ValidationError
from django.db import models

from backend.models.finding import Severity
from pecoret.core.models import TimestampedModel, CASCADE_USER_TO_GHOST


class Status(models.IntegerChoices):
    OPEN = 0, 'Open'
    FIXED = 1, 'Fixed'
    WONT_FIX = 2, 'Wont Fix'


class FindingQuerySet(models.QuerySet):
    def for_program(self, program):
        return self.filter(program=program)

    def filter_unique(self, program, name, target, severity):
        return self.for_program(program).filter(name=name, target=target, severity=Severity[severity.upper()].value)


class Finding(TimestampedModel):
    objects = FindingQuerySet.as_manager()
    name = models.CharField(max_length=256)
    severity = models.PositiveSmallIntegerField(choices=Severity.choices)
    cwe = models.ForeignKey('backend.CWE', on_delete=models.CASCADE, related_name='asmonitor_finding_set', null=True,
                            blank=True)
    user = models.ForeignKey("backend.User", on_delete=CASCADE_USER_TO_GHOST, related_name='asmonitor_finding_set')
    description = models.TextField(blank=True)
    proof_text = models.TextField(default="", blank=True)
    recommendation = models.TextField(blank=True)
    target = models.ForeignKey('asmonitor.Target', on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.OPEN)
    program = models.ForeignKey('asmonitor.Program', on_delete=models.CASCADE)
    tags = models.ManyToManyField('asmonitor.Tag', blank=True)
    internal_information = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date_created']

    def clean(self):
        if self.target.program.pk != self.program.pk:
            raise ValidationError({"target": "target does not belong to project"})
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.program.save()
