from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from backend.models.finding import Finding
from .base import BaseAsset


class WebApplication(BaseAsset):
    """Asset ``WebApplication``
    this asset is mainly used in web application pentests.
    """
    name = models.CharField(max_length=256)
    base_url = models.URLField()
    version = models.CharField(max_length=128, blank=True, null=True)
    findings = GenericRelation(Finding, object_id_field='component_object_id',
                               related_query_name="web_application",
                               content_type_field='component_content_type')
    checklists = GenericRelation('checklists.AssetChecklist', object_id_field='component_object_id',
                                 related_query_name="web_application",
                                 content_type_field='component_content_type')
    asset_type = "web_application"

    class Meta:
        ordering = ["-pk"]
        unique_together = [
            ("project", "name")
        ]
        verbose_name = "Web Application"
        verbose_name_plural = "Web Applications"

    @property
    def get_asset_type_display(self):
        return self._meta.verbose_name

    @property
    def value(self):
        return self.base_url

    def __str__(self):
        return self.name
