from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from backend.models.finding import Finding
from .base import BaseAsset


class Host(BaseAsset):
    ip = models.GenericIPAddressField()
    dns = models.CharField(max_length=255, null=True, blank=True)
    operating_system = models.CharField(max_length=255, null=True, blank=True)
    findings = GenericRelation(Finding, object_id_field='component_object_id',
                               related_query_name="host",
                               content_type_field='component_content_type')
    checklists = GenericRelation('checklists.AssetChecklist', object_id_field='component_object_id',
                                 related_query_name="host",
                                 content_type_field='component_content_type')
    asset_type = "host"

    class Meta:
        ordering = ["-pk"]
        constraints = [
            models.UniqueConstraint(
                fields=["project", "ip"], name="host_ip_unique"
            )
        ]

    @property
    def get_asset_type_display(self):
        return "Host"

    @property
    def name(self):
        return self.__str__()

    @property
    def value(self):
        return self.name

    def __str__(self):
        if not self.dns:
            return self.ip
        return f"{self.dns} ({self.ip})"
