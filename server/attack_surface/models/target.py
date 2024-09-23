import ipaddress
import re
from django.core.exceptions import ValidationError
from django.db import models

from pecoret.core.models import TimestampedModel

DOMAIN_REGEX = r'^(?:[a-zA-Z0-9-]+\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
SUBDOMAIN_REGEX = r'^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'


class ScopeChoices(models.IntegerChoices):
    IN_SCOPE = 0, 'In Scope'
    UNDEFINED = 1, 'Undefined'
    OUT_OF_SCOPE = 2, 'Out of Scope'


class DataTypes(models.IntegerChoices):
    IP = 0, 'IP'
    # NETWORK = 1, 'Network'
    DOMAIN = 2, 'Domain'
    SUBDOMAIN = 3, 'Subdomain'


class TargetQuerySet(models.QuerySet):
    def for_program(self, program):
        return self.filter(program=program)

    def with_data_type_ip(self):
        return self.filter(data_type=DataTypes.IP)

    def exclude_data_type_ip(self):
        return self.exclude(data_type=DataTypes.IP)

    def filter_unique(self, data, program):
        return self.for_program(program).filter(data=data)


class Target(TimestampedModel):
    objects = TargetQuerySet.as_manager()
    data = models.CharField(max_length=512, db_index=True)
    scope = models.PositiveSmallIntegerField(choices=ScopeChoices.choices, default=ScopeChoices.UNDEFINED)
    program = models.ForeignKey('attack_surface.Program', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    data_type = models.PositiveSmallIntegerField(choices=DataTypes.choices)
    host = models.ForeignKey('attack_surface.Host', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-date_updated', 'data']
        unique_together = [
            ('data', 'program')
        ]

    @property
    def display_name(self):
        return self.data

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.program.save()

    def clean(self):
        if self.data_type == DataTypes.IP:
            try:
                ipaddress.ip_address(self.data)
            except ValueError:
                raise ValidationError({'data': 'Invalid IP'})
        elif self.data_type == DataTypes.DOMAIN:
            if not re.match(DOMAIN_REGEX, self.data):
                raise ValidationError({'data': 'Invalid domain'})
        elif self.data_type == DataTypes.SUBDOMAIN:
            if not re.match(SUBDOMAIN_REGEX, self.data):
                raise ValidationError({'data': 'Invalid subdomain'})
        return super().clean()
