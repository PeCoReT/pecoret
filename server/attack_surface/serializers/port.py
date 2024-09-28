from rest_framework import serializers

from attack_surface.models.port import Port, Protocol, PortStatus
from backend.serializers.technology import FlatTechnologySerializer
from pecoret.core.serializers import PrimaryKeyRelatedField, ValuedChoiceField
from .host import HostSerializer
from .tag import TagSerializer


class PortSerializer(serializers.ModelSerializer):
    protocol = ValuedChoiceField(choices=Protocol.choices)
    tags = PrimaryKeyRelatedField(serializer=TagSerializer, many=True, required=False)
    technologies = PrimaryKeyRelatedField(serializer=FlatTechnologySerializer, many=True, required=False)
    host = PrimaryKeyRelatedField(serializer=HostSerializer)
    status = ValuedChoiceField(choices=PortStatus.choices, required=False)

    class Meta:
        model = Port
        fields = [
            'pk', 'date_created', 'date_updated', 'technologies', 'tags', 'number', 'status',
            'service_name', 'protocol', 'host', 'display_name', 'uses_encryption', 'is_web'
        ]
