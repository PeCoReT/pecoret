import secrets
from django.db import models
from pecoret.core.models import TimestampedModel


class Scanner(TimestampedModel):
    name = models.CharField(max_length=255, unique=True)
    scan_types = models.ManyToManyField('attack_surface.ScanType')
    last_seen = models.DateTimeField(null=True, blank=True)
    token = models.CharField(max_length=255, default=secrets.token_urlsafe, editable=False)
