from django.db import models
from pecoret.core.models import TimestampedModel


class ScopeChoices(models.IntegerChoices):
    IN_SCOPE = 0, 'In Scope'
    UNDEFINED = 1, 'Undefined'
    OUT_OF_SCOPE = 2, 'Out of Scope'


class HostQuerySet(models.QuerySet):
    def for_program(self, program):
        return self.filter(program=program)


class Host(TimestampedModel):
    objects = HostQuerySet.as_manager()
    ip = models.GenericIPAddressField()
    technologies = models.ManyToManyField('backend.Technology', blank=True, related_name='asmonitor_hosts')
    description = models.TextField(blank=True, null=True)
    program = models.ForeignKey('asmonitor.Program', on_delete=models.CASCADE)
    last_seen = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField('asmonitor.Tag', blank=True)
    scope = models.PositiveSmallIntegerField(choices=ScopeChoices.choices, default=ScopeChoices.UNDEFINED)

    class Meta:
        ordering = ['-last_seen', 'ip']
        unique_together = [
            ('program', 'ip')
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # update date_updated in program too
        self.program.save()

    @property
    def port_count(self):
        return self.port_set.count()
