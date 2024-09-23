from django.db import models
from django.core.exceptions import ValidationError
from djangoql.queryset import DjangoQLQuerySet
from pecoret.core.models import TimestampedModel
from attack_surface.utils.djangoql import PortQLSchema


class ServiceQuerySet(DjangoQLQuerySet):
    djangoql_schema = PortQLSchema

    def is_web(self, value):
        if value is True:
            return self.filter(port__service_name__in=['http', 'https'])
        return self.exclude(port__service_name__in=['http', 'https'])

    def filter_unique(self, port, target):
        return self.filter(port=port, target=target)


class Service(TimestampedModel):
    objects = ServiceQuerySet.as_manager()
    port = models.ForeignKey('attack_surface.Port', on_delete=models.CASCADE)
    target = models.ForeignKey('attack_surface.Target', on_delete=models.CASCADE)
    banner = models.TextField(null=True, blank=True)
    technologies = models.ManyToManyField('backend.Technology', blank=True)
    tags = models.ManyToManyField('attack_surface.Tag', blank=True)

    # SSL/TLS certificate details (for TLS/SSL services)
    cert_issuer = models.CharField(max_length=255, blank=True, null=True)  # Certificate issuer
    cert_subject = models.CharField(max_length=255, blank=True, null=True)  # Certificate subject (domain)
    cert_valid_from = models.DateTimeField(null=True, blank=True)  # Certificate valid from
    cert_expiry = models.DateTimeField(null=True, blank=True)  # Certificate expiration date
    cert_fingerprint = models.CharField(max_length=64, blank=True, null=True)  # SHA-256 certificate fingerprint
    cert_public_key_info = models.CharField(max_length=255, blank=True,
                                            null=True)  # Public key details (e.g., RSA 2048 Public Key)
    cert_san = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = (('port', 'target'),)
        ordering = ['-date_updated']

    @property
    def program(self):
        return self.target.program

    @property
    def display_name(self):
        return self.scheme

    @property
    def scheme(self):
        return f'{self.port.service_name}://{self.target.data}:{self.port.number}'

    @property
    def is_web(self):
        if self.port.service_name in ['http', 'https']:
            return True
        return False

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        if self.port.host.pk != self.target.host.pk:
            raise ValidationError({'port': 'Port does not belong to host'})
        return super().clean()
