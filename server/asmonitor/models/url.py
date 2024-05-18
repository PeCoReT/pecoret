from django.db import models
from pecoret.core.models import TimestampedModel


class URLQuerySet(models.QuerySet):
    def for_target(self, target):
        return self.filter(target=target)


class URL(TimestampedModel):
    objects = URLQuerySet.as_manager()
    target = models.ForeignKey('asmonitor.Target', on_delete=models.CASCADE)
    url = models.URLField()
    last_seen = models.DateTimeField(blank=True, null=True)
    request = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    status_code = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['url', '-date_updated']
        unique_together = [
            ('target', 'url')
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # update parents
        self.target.save()

    @property
    def program(self):
        return self.target.program
