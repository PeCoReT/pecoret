from rest_framework import serializers
from pecoret.core.serializers import PrimaryKeyRelatedField
from asmonitor.models import Target
from asmonitor.serializers.tag import TagSerializer
from backend.serializers.technology import TechnologySerializer
from .program import ProgramSerializer


class TargetSerializer(serializers.ModelSerializer):
    technologies = PrimaryKeyRelatedField(serializer=TechnologySerializer, many=True, required=False)
    tags = PrimaryKeyRelatedField(serializer=TagSerializer, many=True, required=False)

    class Meta:
        model = Target
        fields = [
            'pk', 'name', 'ip', 'description', 'technologies', 'tags', 'date_updated', 'date_created'
        ]


class GlobalTargetSerializer(TargetSerializer):
    program = PrimaryKeyRelatedField(serializer=ProgramSerializer)

    class Meta:
        model = Target
        fields = TargetSerializer.Meta.fields + ['program']
