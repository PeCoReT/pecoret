from django.db import models
from pecoret.core.models import TimestampedModel


class ScopeQuerySet(models.QuerySet):
    def for_program(self, program):
        return self.filter(program=program)


class Scope(TimestampedModel):
    objects = ScopeQuerySet.as_manager()
    name = models.CharField(max_length=255)
    program = models.ForeignKey('attack_surface.Program', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', '-date_created']
