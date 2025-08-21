from django.db import models
from django.utils.translation import gettext as _

from pecoret.core.models import PeCoReTBaseModel


class Environment(models.IntegerChoices):
    UNKNOWN = 0, _("Unknown")
    PRODUCTION = 1, _("Production")
    TESTING = 2, _("Testing")
    DEVELOPMENT = 3, _("Development")
    STAGING = 4, _("Staging")


class AssetAccessibility(models.IntegerChoices):
    ACCESSIBLE = 0, _("Accessible")
    NOT_ACCESSIBLE = 1, _("Not Accessible")
    UNKNOWN = 2, _("Unknown")


class BaseAssetQuerySet(models.QuerySet):
    def for_project(self, project):
        return self.filter(project=project)


class Asset(PeCoReTBaseModel):
    objects = BaseAssetQuerySet.as_manager()
    project = models.ForeignKey("backend.Project", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    accessible = models.PositiveSmallIntegerField(
        default=AssetAccessibility.UNKNOWN, choices=AssetAccessibility.choices
    )
    description = models.TextField(blank=True, null=True)
    environment = models.PositiveSmallIntegerField(
        choices=Environment.choices, default=Environment.UNKNOWN
    )
    technologies = models.ManyToManyField('backend.Technology', blank=True)
    name = models.CharField(max_length=255)
    asset_type = models.ForeignKey('AssetType', on_delete=models.PROTECT)

    class Meta:
        unique_together = [('name', 'project',)]
        ordering = ['-date_updated', 'name']

    def __str__(self):
        return self.name
