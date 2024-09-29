from django.core.validators import RegexValidator
from django.db import models


class AllowedObjectTypes(models.TextChoices):
    HOST = 'host', 'Host'
    PORT = 'port', 'Port'
    SERVICE = 'service', 'Service'
    TARGET = 'target', 'Target'
    URL = 'url', 'URL'


class ScanTypeQuerySet(models.QuerySet):
    def for_asset(self, asset):
        if 'attack_surface' not in asset._meta.label:
            return self.none()
        return self.filter(allowed_object_type=asset._meta.model_name)

    def enabled(self):
        """ only return scan types with status enabled=true"""
        return self.filter(enabled=True)


class ScanType(models.Model):
    objects = ScanTypeQuerySet.as_manager()
    name = models.CharField(max_length=255, help_text='e.g. Port scan, tech detection, ...', unique=True,
                            validators=[RegexValidator(regex=r'^[A-Za-z0-9\-]+$', )])
    description = models.TextField(blank=True, null=True)
    can_run_manually = models.BooleanField(default=True)
    allowed_object_type = models.CharField(max_length=64, choices=AllowedObjectTypes.choices)
    conditions = models.TextField(blank=True, null=True)
    priority = models.PositiveSmallIntegerField(default=5)
    enabled = models.BooleanField(default=True)

    class Meta:
        ordering = ['-priority', 'name']
