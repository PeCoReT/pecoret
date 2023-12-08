from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from backend.models.finding import Finding
from .base import BaseAsset


class GenericAsset(BaseAsset):
    name = models.CharField(max_length=255)
    findings = GenericRelation(Finding, object_id_field='component_object_id',
                               related_query_name="generic_asset",
                               content_type_field='component_content_type')
    checklists = GenericRelation('checklists.AssetChecklist', object_id_field='component_object_id',
                                 related_query_name="generic_asset",
                                 content_type_field='component_content_type')
    asset_type = 'generic_asset'

    class Meta:
        ordering = ['-pk']
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'name'], name='generic_asset_unique_name'
            )
        ]

    @property
    def get_asset_type_display(self):
        return 'Generic'

    def __str__(self):
        return self.name
