from django.core import validators
from django.db import models
from pecoret.core.models import TimestampedModel


class HostnameQuerySet(models.QuerySet):
    def for_program(self, program):
        return self.filter(program=program)

    def for_host(self, host):
        return self.filter(host=host)


class Hostname(TimestampedModel):
    objects = HostnameQuerySet.as_manager()
    name = models.CharField(max_length=512, validators=[validators.RegexValidator(
        regex=r'^(?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?'
              r'(?:\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\.?$')])
    host = models.ForeignKey('asmonitor.Host', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        unique_together = [
            ('name', 'host')
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.host.save()
