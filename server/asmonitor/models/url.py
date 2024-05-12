from django.db import models
from pecoret.core.models import TimestampedModel


class URLQuerySet(models.QuerySet):
    def for_host(self, host):
        return self.filter(host=host)


class URL(TimestampedModel):
    objects = URLQuerySet.as_manager()
    host = models.ForeignKey('asmonitor.Host', on_delete=models.CASCADE)
    url = models.URLField()
    last_seen = models.DateTimeField(blank=True, null=True)
    request = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    status_code = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['url', '-date_updated']
        unique_together = [
            ('host', 'url')
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # update parents
        self.host.save()

    @property
    def program(self):
        return self.host.program
