import secrets
from django.db import models
from pecoret.core.models import TimestampedModel


class Scanner(TimestampedModel):
    name = models.CharField(max_length=255, unique=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    token = models.CharField(max_length=255, default=secrets.token_urlsafe, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-last_seen']
