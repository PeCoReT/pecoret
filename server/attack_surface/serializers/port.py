from rest_framework import serializers
from pecoret.core.serializers import PrimaryKeyRelatedField, ValuedChoiceField
from attack_surface.models.port import Port, Protocol
from .target import TargetSerializer


class PortSerializer(serializers.ModelSerializer):
    target = PrimaryKeyRelatedField(serializer=TargetSerializer)
    protocol = ValuedChoiceField(choices=Protocol.choices)

    class Meta:
        model = Port
        fields = [
            'pk', 'date_created', 'date_updated', 'last_seen', 'target', 'port',
            'service', 'protocol', 'banner'
        ]
