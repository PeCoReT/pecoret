from django.core.validators import RegexValidator
from django.db import models


class AllowedObjectTypes(models.TextChoices):
    HOST = 'host', 'Host'
    PORT = 'port', 'Port'
    SERVICE = 'service', 'Service'
    TARGET = 'target', 'Target'
    URL = 'url', 'URL'


class ScanType(models.Model):
    name = models.CharField(max_length=255, help_text='e.g. Port scan, tech detection, ...', unique=True,
                            validators=[RegexValidator(regex=r'^[A-Za-z0-9\-]+$', )])
    description = models.TextField(blank=True, null=True)
    can_run_manually = models.BooleanField(default=True)
    allowed_object_type = models.CharField(max_length=64, choices=AllowedObjectTypes.choices)
    conditions = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']
