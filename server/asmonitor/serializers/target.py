from rest_framework import serializers

from asmonitor.models import Target
from asmonitor.serializers.tag import TagSerializer
from backend.serializers.technology import TechnologySerializer
from pecoret.core.serializers import PrimaryKeyRelatedField


class TargetSerializer(serializers.ModelSerializer):
    technologies = PrimaryKeyRelatedField(serializer=TechnologySerializer, many=True, required=False)
    tags = PrimaryKeyRelatedField(serializer=TagSerializer, many=True, required=False)

    class Meta:
        model = Target
        fields = [
            'pk', 'name', 'ip', 'description', 'technologies', 'tags', 'date_updated', 'date_created'
        ]
