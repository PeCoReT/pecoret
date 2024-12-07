from django.db import models

from core.custom_fields.models import CustomField, CustomFieldValue, CustomFieldQuerySet


class CustomFieldAssetQuerySet(CustomFieldQuerySet):
    def for_asset_type(self, asset_type):
        return self.filter(asset_types=asset_type)


class CustomFieldAsset(CustomField):
    objects = CustomFieldAssetQuerySet.as_manager()
    asset_types = models.ManyToManyField('backend.AssetType', blank=True)


class CustomFieldAssetValueQuerySet(models.QuerySet):
    def for_project(self, project):
        return self.filter(asset__project=project)

    def for_asset(self, asset):
        return self.filter(asset=asset)

class CustomFieldAssetValue(CustomFieldValue):
    objects = CustomFieldAssetValueQuerySet.as_manager()
    asset = models.ForeignKey('backend.Asset', on_delete=models.CASCADE)
    field = models.ForeignKey('backend.CustomFieldAsset', on_delete=models.CASCADE)

    class Meta:
        unique_together = [('asset', 'field')]
        ordering = ['-date_created']
