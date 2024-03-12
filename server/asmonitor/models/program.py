from django.db import models
from pecoret.core.models import TimestampedModel


class Program(TimestampedModel):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name
