from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models
from djangoql.queryset import DjangoQLQuerySet

from attack_surface.utils.djangoql import PecoQLSchema
from  .base import BaseAssetModel


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


class Service(BaseAssetModel):
    objects = ServiceQuerySet.as_manager()
    target = models.ForeignKey('attack_surface.Target', on_delete=models.CASCADE)
    port_number = models.PositiveSmallIntegerField(validators=[MaxValueValidator(65535)])
    service_name = models.CharField(max_length=32, validators=[RegexValidator(regex='^[a-zA-Z0-9]+$')])
    protocol = models.PositiveSmallIntegerField(choices=Protocol.choices, default=Protocol.TCP)
    uses_encryption = models.BooleanField(default=False, help_text='Uses TLS/SSL encryption')
    port_status = models.PositiveSmallIntegerField(choices=PortStatus.choices, default=PortStatus.OPEN)

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
    scan_objects = GenericRelation('attack_surface.ScanObject', related_query_name='services')

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
