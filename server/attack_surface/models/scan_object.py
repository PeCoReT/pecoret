from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models


class ScanObject(models.Model):
    """Tracks which objects are scanned in each scan."""
    scan = models.ForeignKey('attack_surface.Scan', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    asset = GenericForeignKey('content_type', 'object_id')

    def clean(self):
        allowed_type = self.scan.scan_type.allowed_object_type
        # validate that the target type is allowed by the scan type
        if self.content_type.model != allowed_type:
            raise ValidationError({'target': f"Invalid target type '{self.content_type.model}' for scan type "
                                             f"'{self.scan.scan_type.name}'. Expected '{allowed_type}'."})
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
