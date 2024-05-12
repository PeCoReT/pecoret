import ipaddress

from django.db import models
from django.core.exceptions import ValidationError
from pecoret.core.models import TimestampedModel


class ScopeTypes(models.IntegerChoices):
    IP = 0, 'IP'
    NETWORK = 1, 'Network'
    DOMAIN = 2, 'Domain'
    WILDCARD_DOMAIN = 3, 'Wildcard'
    SUBDOMAIN = 4, 'Subdomain'


class ScopeQuerySet(models.QuerySet):
    def for_program(self, program):
        return self.filter(program=program)


class Scope(TimestampedModel):
    objects = ScopeQuerySet.as_manager()
    data = models.CharField(max_length=512)
    program = models.ForeignKey('asmonitor.Program', on_delete=models.CASCADE)
    scope_type = models.PositiveSmallIntegerField(choices=ScopeTypes.choices)

    class Meta:
        ordering = ['-date_updated']
        unique_together = [
            ('program', 'data')
        ]

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        if self.scope_type == ScopeTypes.IP:
            try:
                ipaddress.ip_address(self.data)
            except ValueError:
                raise ValidationError({'data': 'Invalid IP'})
        elif self.scope_type == ScopeTypes.NETWORK:
            try:
                ipaddress.ip_network(self.data)
            except ValueError:
                raise ValidationError({'data': 'Invalid network'})
        return super().clean()
