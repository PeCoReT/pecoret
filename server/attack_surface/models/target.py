import ipaddress
from django.db import models
from django.core.exceptions import ValidationError
from pecoret.core.models import TimestampedModel


class ScopeChoices(models.IntegerChoices):
    IN_SCOPE = 0, 'In Scope'
    UNDEFINED = 1, 'Undefined'
    OUT_OF_SCOPE = 2, 'Out of Scope'


class DataTypes(models.IntegerChoices):
    IP = 0, 'IP'
    NETWORK = 1, 'Network'
    DOMAIN = 2, 'Domain'
    SUBDOMAIN = 3, 'Subdomain'


class TargetQuerySet(models.QuerySet):
    def for_program(self, program):
        return self.filter(program=program)


class Target(TimestampedModel):
    objects = TargetQuerySet.as_manager()
    first_seen = models.DateTimeField(blank=True, null=True)
    last_seen = models.DateTimeField(blank=True, null=True)
    data = models.CharField(max_length=512, db_index=True)
    scope = models.PositiveSmallIntegerField(choices=ScopeChoices.choices, default=ScopeChoices.UNDEFINED)
    tags = models.ManyToManyField('attack_surface.Tag', blank=True)
    program = models.ForeignKey('attack_surface.Program', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    technologies = models.ManyToManyField('backend.Technology', blank=True)
    data_type = models.PositiveSmallIntegerField(choices=DataTypes.choices)

    class Meta:
        ordering = ['-last_seen', 'data']
        unique_together = [
            ('data', 'program')
        ]

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.program.save()

    def clean(self):
        if self.data_type == DataTypes.IP:
            try:
                ipaddress.ip_address(self.data)
            except ValueError:
                raise ValidationError({'name': 'Invalid IP'})
        elif self.data_type == DataTypes.NETWORK:
            try:
                ipaddress.ip_network(self.data)
            except ValueError:
                raise ValidationError({'name': 'Invalid network'})
        return super().clean()
