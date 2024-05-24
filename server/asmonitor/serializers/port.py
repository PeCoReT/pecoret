from rest_framework import serializers
from pecoret.core.serializers import ValuedChoiceField
from pecoret.core.serializers import PrimaryKeyRelatedField
from asmonitor.models.port import Port, Protocol
from .program import ProgramSerializer
from .target import TargetSerializer


class PortSerializer(serializers.ModelSerializer):
    protocol = ValuedChoiceField(choices=Protocol.choices)

    class Meta:
        model = Port
        fields = [
            'pk', 'port', 'banner', 'service', 'date_created', 'date_updated', 'protocol'
        ]


class GlobalPortSerializer(PortSerializer):
    program = PrimaryKeyRelatedField(serializer=ProgramSerializer)
    target = PrimaryKeyRelatedField(serializer=TargetSerializer)

    class Meta:
        model = Port
        fields = PortSerializer.Meta.fields + ['program', 'target']
