from urllib.parse import urlparse
from django.db import models
from pecoret.core.models import TimestampedModel


class URLQuerySet(models.QuerySet):
    def for_program(self, program):
        return self.filter(program=program)

    def filter_unique(self, url, program):
        return self.for_program(program).filter(url=url)


class URL(TimestampedModel):
    objects = URLQuerySet.as_manager()
    program = models.ForeignKey('attack_surface.Program', on_delete=models.CASCADE)
    url = models.URLField()
    last_seen = models.DateTimeField(blank=True, null=True)
    request = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    status_code = models.PositiveSmallIntegerField(blank=True, null=True)
    is_base = models.BooleanField(editable=False)
    tags = models.ManyToManyField('attack_surface.Tag', blank=True)
    technologies = models.ManyToManyField('backend.Technology', blank=True)

    class Meta:
        ordering = ['-date_updated', 'url']
        unique_together = [
            ('program', 'url')
        ]

    def save(self, *args, **kwargs):
        if self.is_base is None:
            self.is_base = self.calculate_is_base()
        super().save(*args, **kwargs)
        # update parents
        self.program.save()

    def calculate_is_base(self):
        parsed = urlparse(self.url)
        # handle special case when url ends with ? urlparse does not set query
        if self.url[-1] == '?' and not parsed.query:
            return False
        if parsed.query or parsed.fragment or parsed.path:
            return False
        return True
