from urllib.parse import urlparse

from django.core.exceptions import ValidationError
from django.db import models
from djangoql.queryset import DjangoQLQuerySet

from attack_surface.utils.djangoql import PecoQLSchema
from pecoret.core.models import TimestampedModel
from .target import ScopeChoices


class URLQuerySet(DjangoQLQuerySet):
    djangoql_schema = PecoQLSchema

    def for_program(self, program):
        return self.filter(service__target__program=program)

    def exclude_programs(self, programs):
        return self.exclude(service__target__program__in=programs)

    def filter_unique(self, url, service):
        return self.filter(url=url, service=service)

    def in_scope(self):
        return self.filter(service__target__scope=ScopeChoices.IN_SCOPE)

    def get_unique_program_pks(self):
        return self.values_list('service__target__program__pk', flat=True).order_by(
            'service__target__program__pk').distinct()


class URL(TimestampedModel):
    objects = URLQuerySet.as_manager()
    service = models.ForeignKey('attack_surface.Service', on_delete=models.CASCADE)
    url = models.URLField(db_index=True)
    request = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    status_code = models.PositiveSmallIntegerField(blank=True, null=True)
    is_base = models.BooleanField(editable=False)
    tags = models.ManyToManyField('attack_surface.Tag', blank=True)
    technologies = models.ManyToManyField('backend.Technology', blank=True)
    favicon_hash = models.CharField(max_length=128, blank=True, null=True)
    fuzzy_hash_body = models.CharField(max_length=512, blank=True, null=True)
    fuzzy_hash_headers = models.CharField(max_length=512, blank=True, null=True)
    body_hash = models.CharField(max_length=512, blank=True, null=True)
    title = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        ordering = ['-date_updated', 'url']
        unique_together = [
            ('service', 'url')
        ]

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        if self.is_base is None:
            self.is_base = self.calculate_is_base()
        self.full_clean()
        super().save(*args, **kwargs)
        # update parents
        self.service.target.program.save()

    def calculate_is_base(self):
        parsed = urlparse(self.url)
        # handle special case when url ends with ? urlparse does not set query
        if self.url[-1] == '?' and not parsed.query:
            return False
        if parsed.query or parsed.fragment or parsed.path != "/":
            return False
        return True

    @property
    def program(self):
        return self.service.target.program

    @property
    def display_name(self):
        return self.url

    def clean(self):
        if not self.service.is_web:
            raise ValidationError({'service': 'Service is not a web service'})
        return super().clean()

    @property
    def is_in_scope(self):
        return self.service.target.is_in_scope
