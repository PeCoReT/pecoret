from pecoret.core.models import TimestampedModel
from rest_framework.exceptions import ValidationError

from attack_surface.models.scan import ScanStatus


class BaseAssetModel(TimestampedModel):
    def delete(self, *args, **kwargs):
        if self.scan_objects.filter(scan__status=ScanStatus.RUNNING).exists():
            raise ValidationError({'pk': 'Running scans cannot be deleted.'})
        return super().delete(*args, **kwargs)

    class Meta:
        abstract = True
