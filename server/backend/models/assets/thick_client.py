from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from backend.models.finding import Finding
from .base import BaseAsset


class OperatingSystem(models.IntegerChoices):
    UNKNOWN = 0, "Unknown"
    WINDOWS = 1, "Windows"
    LINUX = 2, "Linux"


class DecompileAllowedChoices(models.IntegerChoices):
    UNKNOWN = 0, "Unknown"
    YES = 1, "Yes"
    NO = 2, "No"


class ThickClient(BaseAsset):
    """
    asset model for ``ThickClient``.
    """
    name = models.CharField(max_length=256)
    version = models.CharField(max_length=128, blank=True)
    os = models.PositiveSmallIntegerField(choices=OperatingSystem.choices, default=OperatingSystem.UNKNOWN)
    programming_language = models.CharField(max_length=64, default="Unknown")
    decompile_allowed = models.PositiveSmallIntegerField(choices=DecompileAllowedChoices.choices,
                                                         default=DecompileAllowedChoices.UNKNOWN)
    findings = GenericRelation(Finding, object_id_field='component_object_id',
                               related_query_name="thick_client",
                               content_type_field='component_content_type')
    checklists = GenericRelation('checklists.AssetChecklist', object_id_field='component_object_id',
                                 related_query_name="thick_client",
                                 content_type_field='component_content_type')

    asset_type = "thick_client"

    def __str__(self):
        return self.name

    @property
    def value(self):
        return self.value

    @property
    def get_asset_type_display(self):
        return "Thick Client"

    class Meta:
        ordering = ["name", "version"]
        unique_together = [('project', 'name')]
