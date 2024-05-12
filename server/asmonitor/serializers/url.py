from rest_framework import serializers

from asmonitor import utils
from asmonitor.models import URL, Hostname
from asmonitor.models.port import Port, Protocol
from pecoret.core.serializers import PrimaryKeyRelatedField
from .host import HostSerializer
from .program import ProgramSerializer


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = [
            'pk', 'url', 'date_created', 'date_updated', 'last_seen', 'request', 'response', 'status_code'
        ]

    def create(self, validated_data):
        instance = super().create(validated_data)
        scheme, port = utils.url.port_and_scheme_from_url(instance.url)
        _, _ = Port.objects.get_or_create(host=instance.host, port=port, protocol=Protocol.TCP,
                                          defaults={'service': scheme})
        hostname = utils.url.hostname_from_url(instance.url)
        _, _ = Hostname.objects.get_or_create(name=hostname, host=instance.host)
        return instance


class GlobalURLSerializer(URLSerializer):
    program = PrimaryKeyRelatedField(serializer=ProgramSerializer)
    host = PrimaryKeyRelatedField(serializer=HostSerializer)

    class Meta:
        model = URL
        fields = ['pk', 'url', 'date_created', 'date_updated', 'last_seen', 'program', 'status_code', 'host']
