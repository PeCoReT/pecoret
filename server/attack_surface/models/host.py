from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from pecoret.core.models import TimestampedModel


class HostQuerySet(models.QuerySet):
    def filter_unique(self, ip):
        return self.filter(ip_address=ip)


class Host(TimestampedModel):
    objects = HostQuerySet.as_manager()
    ip_address = models.GenericIPAddressField(unique=True)
    date_asn_last_updated = models.DateTimeField(null=True, blank=True)
    asn = models.ForeignKey('attack_surface.ASN', on_delete=models.SET_NULL, null=True, blank=True)
    scan_objects = GenericRelation('attack_surface.ScanObject', related_query_name='hosts')

    @property
    def hostnames(self):
        t = self.target_set.exclude_data_type_ip()
        return list(t.values_list('data', flat=True))

    @property
    def display_name(self):
        return self.ip_address
