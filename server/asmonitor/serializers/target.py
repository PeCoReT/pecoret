from rest_framework import serializers

from asmonitor.models.target import Target, ScopeChoices
from asmonitor.serializers.tag import TagSerializer
from backend.serializers.technology import TechnologySerializer
from pecoret.core.serializers import PrimaryKeyRelatedField, ValuedChoiceField
from .program import ProgramSerializer


class TargetSerializer(serializers.ModelSerializer):
    technologies = PrimaryKeyRelatedField(serializer=TechnologySerializer, many=True, required=False)
    tags = PrimaryKeyRelatedField(serializer=TagSerializer, many=True, required=False)
    scope = ValuedChoiceField(choices=ScopeChoices.choices)
    name = serializers.CharField(required=False)

    class Meta:
        model = Target
        fields = [
            'pk', 'ip', 'description', 'technologies', 'tags', 'date_updated', 'date_created', 'last_seen',
            'port_count', 'scope', 'name', 'display_name'
        ]


class GlobalTargetSerializer(TargetSerializer):
    program = PrimaryKeyRelatedField(serializer=ProgramSerializer)

    class Meta:
        model = Target
        fields = TargetSerializer.Meta.fields + ['program']
