from django.db import models

from pecoret.core.models import TimestampedModel


class TargetQuerySet(models.QuerySet):
    def for_program(self, program):
        return self.filter(program=program)


class Target(TimestampedModel):
    objects = TargetQuerySet.as_manager()
    name = models.CharField(max_length=512)
    ip = models.GenericIPAddressField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    technologies = models.ManyToManyField('backend.Technology', blank=True)
    last_seen = models.DateTimeField(blank=True, null=True)
    program = models.ForeignKey('asmonitor.Program', on_delete=models.CASCADE)
    tags = models.ManyToManyField('asmonitor.Tag', blank=True)

    class Meta:
        ordering = ['-last_seen', 'name']
        unique_together = [
            ('name', 'program', 'ip')
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # update date_updated in program too
        self.program.save()
