from django.core.validators import RegexValidator
from django.db import models
from pecoret.core.models import TimestampedModel


class ASNQuerySet(models.QuerySet):
    def filter_unique(self, value):
        return self.filter(value=value)


class ASN(TimestampedModel):
    objects = ASNQuerySet.as_manager()
    country = models.CharField(max_length=255)
    country_code = models.CharField(max_length=8)
    region = models.CharField(max_length=255)
    region_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=32, null=True, blank=True)
    timezone = models.CharField(max_length=128, null=True, blank=True)
    isp = models.CharField(max_length=255, null=True, blank=True)
    organization = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=32, validators=[RegexValidator(regex=r'^AS[0-9]+$')], unique=True)

    class Meta:
        ordering = ['value']
