from urllib.parse import urlparse
from django.db import models
from pecoret.core.models import TimestampedModel


class URLQuerySet(models.QuerySet):
    def for_target(self, target):
        return self.filter(target=target)

    def filter_unique(self, url, target):
        return self.for_target(target).filter(url=url)


class URL(TimestampedModel):
    objects = URLQuerySet.as_manager()
    target = models.ForeignKey('asmonitor.Target', on_delete=models.CASCADE)
    url = models.URLField()
    last_seen = models.DateTimeField(blank=True, null=True)
    request = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    status_code = models.PositiveSmallIntegerField(blank=True, null=True)
    is_base = models.BooleanField(editable=False, null=True)

    class Meta:
        ordering = ['url', '-date_updated']
        unique_together = [
            ('target', 'url')
        ]

    def save(self, *args, **kwargs):
        if self.is_base is None:
            self.is_base = self.calculate_is_base()
        super().save(*args, **kwargs)
        # update parents
        self.target.save()

    @property
    def program(self):
        return self.target.program

    def calculate_is_base(self):
        url = self.url
        parsed = urlparse(url)
        port = 80
        if parsed.port:
            port = parsed.port
        if parsed.scheme == "https":
            port = 443
        base_url = f"{parsed.scheme}://{parsed.netloc}:{port}"
        if f':{port}' not in url:
            url = f"{parsed.scheme}://{parsed.netloc}:{port}"
        if base_url == url:
            return True
        return False
