from django.core.validators import MaxValueValidator, RegexValidator
from djangoql.queryset import DjangoQLQuerySet
from django.db import models
from attack_surface.utils.djangoql import PortQLSchema
from pecoret.core.models import TimestampedModel


WEB_SERVICES = [
    'http', 'https'
]

class Protocol(models.IntegerChoices):
    TCP = 0, 'TCP'
    UDP = 1, 'UDP'


class PortStatus(models.IntegerChoices):
    OPEN = 0, 'Open'
    CLOSED = 1, 'Closed'


class PortQuerySet(DjangoQLQuerySet):
    djangoql_schema = PortQLSchema

    def for_host(self, host):
        return self.filter(host=host)

    def for_target(self, target):
        return self.filter(host__target=target)

    def is_web(self, value):
        if value is True:
            return self.filter(service_name__in=WEB_SERVICES)
        return self.filter()

    def filter_unique(self, number, protocol, host):
        return self.for_host(host).filter(number=number, protocol=Protocol[protocol].value)


class Port(TimestampedModel):
    objects = PortQuerySet.as_manager()
    host = models.ForeignKey('attack_surface.Host', on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(validators=[MaxValueValidator(65535)])
    service_name = models.CharField(max_length=32, validators=[RegexValidator(regex='^[a-zA-Z0-9]+$')])
    protocol = models.PositiveSmallIntegerField(choices=Protocol.choices, default=Protocol.TCP)
    uses_encryption = models.BooleanField(default=False, help_text='Uses TLS/SSL encryption')
    status = models.PositiveSmallIntegerField(choices=PortStatus.choices, default=PortStatus.OPEN)

    class Meta:
        unique_together = [
            ('host', 'number', 'protocol')
        ]
        ordering = ['number', 'protocol']

    @property
    def display(self):
        return f'{self.get_protocol_display().lower()}/{str(self.number)}/{self.service_name}'

    @property
    def is_web(self):
        return self.service_name in WEB_SERVICES
