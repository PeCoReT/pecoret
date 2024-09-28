from rest_framework import serializers

from attack_surface.models import Host
from pecoret.core.serializers import PrimaryKeyRelatedField
from .asn import ASNSerializer


class HostSerializer(serializers.ModelSerializer):
    asn = PrimaryKeyRelatedField(serializer=ASNSerializer, required=False, allow_null=True)

    class Meta:
        model = Host
        fields = ['ip_address', 'asn', 'date_asn_last_updated', 'hostnames', 'pk', 'display_name', 'date_updated',
                  'date_created']
