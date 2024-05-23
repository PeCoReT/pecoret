from rest_framework import serializers

from asmonitor import utils
from asmonitor.models import URL
from asmonitor.models.port import Port, Protocol
from pecoret.core.serializers import PrimaryKeyRelatedField
from .program import ProgramSerializer
from .target import TargetSerializer


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = [
            'pk', 'url', 'date_created', 'date_updated', 'last_seen', 'request', 'response', 'status_code',
            'is_base'
        ]

    def create(self, validated_data):
        instance = super().create(validated_data)
        scheme, port = utils.url.port_and_scheme_from_url(instance.url)
        _, _ = Port.objects.get_or_create(target=instance.target, port=port, protocol=Protocol.TCP,
                                          defaults={'service': scheme})
        return instance


class GlobalURLSerializer(URLSerializer):
    program = PrimaryKeyRelatedField(serializer=ProgramSerializer)
    target = PrimaryKeyRelatedField(serializer=TargetSerializer)

    class Meta:
        model = URL
        fields = ['pk', 'url', 'date_created', 'date_updated', 'last_seen', 'program', 'status_code', 'target',
                  'is_base']
