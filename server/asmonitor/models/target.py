from django.db import models
from pecoret.core.models import TimestampedModel


class ScopeChoices(models.IntegerChoices):
    IN_SCOPE = 0, 'In Scope'
    UNDEFINED = 1, 'Undefined'
    OUT_OF_SCOPE = 2, 'Out of Scope'


class TargetQuerySet(models.QuerySet):
    def for_program(self, program):
        return self.filter(program=program)


class Target(TimestampedModel):
    objects = TargetQuerySet.as_manager()
    name = models.CharField(max_length=512, db_index=True)
    ip = models.GenericIPAddressField(null=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    technologies = models.ManyToManyField('backend.Technology', blank=True)
    last_seen = models.DateTimeField(blank=True, null=True)
    program = models.ForeignKey('asmonitor.Program', on_delete=models.CASCADE)
    tags = models.ManyToManyField('asmonitor.Tag', blank=True)
    scope = models.PositiveSmallIntegerField(choices=ScopeChoices.choices, default=ScopeChoices.UNDEFINED)

    class Meta:
        ordering = ['-last_seen', 'name']
        unique_together = [
            ('name', 'program', 'ip')
        ]

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.ip
        super().save(*args, **kwargs)
        # update date_updated in program too
        self.program.save()

    @property
    def port_count(self):
        return self.port_set.count()

    @property
    def display_name(self):
        if self.ip:
            return f'{self.name} ({self.ip})'
        return self.name
