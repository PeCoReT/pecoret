from rest_framework import serializers

from asmonitor.models.host import Host, ScopeChoices
from asmonitor.serializers.tag import TagSerializer
from backend.serializers.technology import TechnologySerializer
from pecoret.core.serializers import PrimaryKeyRelatedField, ValuedChoiceField
from .program import ProgramSerializer


class HostSerializer(serializers.ModelSerializer):
    technologies = PrimaryKeyRelatedField(serializer=TechnologySerializer, many=True, required=False)
    tags = PrimaryKeyRelatedField(serializer=TagSerializer, many=True, required=False)
    scope = ValuedChoiceField(choices=ScopeChoices.choices)

    class Meta:
        model = Host
        fields = [
            'pk', 'ip', 'description', 'technologies', 'tags', 'date_updated', 'date_created', 'last_seen',
            'port_count', 'scope'
        ]


class GlobalHostSerializer(HostSerializer):
    program = PrimaryKeyRelatedField(serializer=ProgramSerializer)

    class Meta:
        model = Host
        fields = HostSerializer.Meta.fields + ['program']
