from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models
from djangoql.queryset import DjangoQLQuerySet

from attack_surface.utils.djangoql import PecoQLSchema
from pecoret.core.models import TimestampedModel
from .target import ScopeChoices


class Protocol(models.IntegerChoices):
    TCP = 0, 'TCP'
    UDP = 1, 'UDP'


class PortStatus(models.IntegerChoices):
    OPEN = 0, 'Open'
    CLOSED = 1, 'Closed'


class ServiceQuerySet(DjangoQLQuerySet):
    djangoql_schema = PecoQLSchema

    def is_web(self, value):
        if value is True:
            return self.filter(service_name__in=['http', 'https'])
        return self.exclude(service_name__in=['http', 'https'])

    def filter_unique(self, port_number, protocol, target):
        return self.filter(port_number=port_number, protocol=Protocol[protocol.upper()].value, target=target)

    def in_scope(self):
        return self.filter(target__scope=ScopeChoices.IN_SCOPE)

    def for_program(self, program):
        return self.filter(target__program=program)

    def exclude_programs(self, programs):
        return self.exclude(target__program__in=programs)

    def get_unique_program_pks(self):
        return self.values_list('target__program__pk', flat=True).order_by(
            'target__program__pk').distinct()


class Service(TimestampedModel):
    objects = ServiceQuerySet.as_manager()
    target = models.ForeignKey('attack_surface.Target', on_delete=models.CASCADE)
    port_number = models.PositiveSmallIntegerField(validators=[MaxValueValidator(65535)], db_index=True)
    service_name = models.CharField(max_length=32, validators=[RegexValidator(regex='^[a-zA-Z0-9]+$')])
    protocol = models.PositiveSmallIntegerField(choices=Protocol.choices, default=Protocol.TCP, db_index=True)
    uses_encryption = models.BooleanField(default=False, help_text='Uses TLS/SSL encryption')
    port_status = models.PositiveIntegerField(choices=PortStatus.choices, default=PortStatus.OPEN)

    banner = models.TextField(null=True, blank=True)
    technologies = models.ManyToManyField('backend.Technology', blank=True)
    tags = models.ManyToManyField('attack_surface.Tag', blank=True)

    # SSL/TLS certificate details (for TLS/SSL services)
    cert_issuer = models.CharField(max_length=255, blank=True, null=True)
    cert_subject = models.CharField(max_length=255, blank=True, null=True)
    cert_valid_from = models.DateTimeField(null=True, blank=True)
    cert_expiry = models.DateTimeField(null=True, blank=True)
    cert_fingerprint = models.CharField(max_length=64, blank=True, null=True)
    cert_public_key_info = models.CharField(max_length=255, blank=True, null=True)
    cert_san = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = (('port_number', 'target', 'protocol'),)
        ordering = ['-date_updated']

    @property
    def program(self):
        return self.target.program

    @property
    def display_name(self):
        return self.scheme

    @property
    def scheme(self):
        return f'{self.service_name}://{self.target.data}:{self.port_number}'

    @property
    def is_web(self):
        if self.service_name in ['http', 'https']:
            return True
        return False

    @property
    def is_in_scope(self):
        return self.target.is_in_scope

    def save(self, *args, **kwargs):
        if self.banner:
            try:
                banner = self.banner.encode().decode('unicode_escape', errors='ignore')
            except UnicodeDecodeError:
                banner = self.banner
            # strip null bytes
            self.banner = banner.replace(r'\x00', '')
        return super().save(*args, **kwargs)
