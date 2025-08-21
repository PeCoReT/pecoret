from django.db import models

from pecoret.core.models import TimestampedModel


class AssetType(TimestampedModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True,
                                   help_text="Description of the asset type. May be used in your report template.")

    def __str__(self):
        return self.name
