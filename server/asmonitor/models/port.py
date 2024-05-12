from django.db import models
from django.core.validators import MaxValueValidator
from pecoret.core.models import TimestampedModel


class Protocol(models.IntegerChoices):
    TCP = 0, "TCP"
    UDP = 1, "UDP"


class PortQuerySet(models.QuerySet):
    def for_host(self, host):
        return self.filter(host=host)


class Port(TimestampedModel):
    objects = PortQuerySet.as_manager()
    host = models.ForeignKey('asmonitor.Host', on_delete=models.CASCADE)
    port = models.PositiveSmallIntegerField(validators=[MaxValueValidator(65535)])
    service = models.CharField(max_length=32, null=True, blank=True)
    protocol = models.PositiveSmallIntegerField(choices=Protocol.choices, default=Protocol.TCP)
    banner = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        unique_together = [
            ('host', 'port', 'protocol')
        ]
        ordering = ['port', 'protocol']
