from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.contenttypes.fields import GenericRelation
from backend.models.finding import Finding
from pecoret.core.models import TimestampedModel


class Protocol(models.IntegerChoices):
    TCP = 0, "TCP"
    UDP = 1, "UDP"


class State(models.IntegerChoices):
    OPEN = 0, "Open"
    CLOSED = 1, "Closed"
    FILTERED = 2, "Filtered"


class ServiceQuerySet(models.QuerySet):
    def for_project(self, project):
        return self.filter(host__project=project)


class Service(TimestampedModel):
    objects = ServiceQuerySet.as_manager()
    name = models.CharField(max_length=256, blank=True)
    host = models.ForeignKey('backend.Host', on_delete=models.CASCADE, related_name="services")
    protocol = models.PositiveSmallIntegerField(choices=Protocol.choices, default=Protocol.TCP)
    port = models.PositiveSmallIntegerField(validators=[MaxValueValidator(65535)], blank=False, null=True)
    product = models.CharField(max_length=255, blank=True, null=True)
    state = models.PositiveSmallIntegerField(choices=State.choices, default=State.OPEN, null=True)
    findings = GenericRelation(Finding, object_id_field='component_object_id',
                               related_query_name="service",
                               content_type_field='component_content_type')
    checklists = GenericRelation('checklists.AssetChecklist', object_id_field='component_object_id',
                                 related_query_name="service",
                                 content_type_field='component_content_type')

    class Meta:
        ordering = ["host__dns", "host__ip", "port"]
        unique_together = [
            ('host', "port", "protocol")
        ]

    def __str__(self):
        return f"{self.name}/{Protocol(self.protocol).name} {self.host.ip}:{self.port}"

    @property
    def value(self):
        return self.display_name

    @property
    def get_asset_type_display(self):
        return "Service"

    @property
    def project(self):
        return self.host.project

    @property
    def display_name(self) -> str:
        return str(self)

    asset_type = "service"
