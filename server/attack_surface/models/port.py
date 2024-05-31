from django.db import models
from django.core.validators import MaxValueValidator
from pecoret.core.models import TimestampedModel


class Protocol(models.IntegerChoices):
    TCP = 0, 'TCP'
    UDP = 1, 'UDP'


class PortQuerySet(models.QuerySet):
    def for_target(self, target):
        return self.filter(target=target)

    def filter_unique(self, protocol, port, target):
        return self.for_target(target).filter(protocol=Protocol[protocol].value, port=port)


class Port(TimestampedModel):
    objects = PortQuerySet.as_manager()
    target = models.ForeignKey('attack_surface.Target', on_delete=models.CASCADE)
    port = models.PositiveSmallIntegerField(validators=[MaxValueValidator(65535)])
    service = models.CharField(max_length=32, null=True, blank=True)
    protocol = models.PositiveSmallIntegerField(choices=Protocol.choices, default=Protocol.TCP)
    banner = models.CharField(max_length=1024, null=True, blank=True)
    last_seen = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = [
            ('target', 'port', 'protocol')
        ]
        ordering = ['port', 'protocol']

    @property
    def program(self):
        return self.target.program
