from rest_framework import serializers
from django_q.tasks import async_task

from pecoret.core.serializers import PrimaryKeyRelatedField
from backend.serializers.technology import TechnologySerializer
from attack_surface.models.url import URL
from attack_surface import tasks
from .program import ProgramSerializer
from .tag import TagSerializer


class URLSerializer(serializers.ModelSerializer):
    technologies = PrimaryKeyRelatedField(serializer=TechnologySerializer, many=True, required=False)
    tags = PrimaryKeyRelatedField(serializer=TagSerializer, many=True, required=False)
    program = PrimaryKeyRelatedField(serializer=ProgramSerializer)

    class Meta:
        model = URL
        fields = [
            'pk', 'date_created', 'date_updated', 'status_code', 'last_seen',
            'request', 'response', 'is_base', 'tags', 'technologies', 'url', 'program'
        ]

    def create(self, validated_data):
        instance = super().create(validated_data)
        async_task(tasks.sync_implicit_techs_url, instance.pk)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        async_task(tasks.sync_implicit_techs_url, instance.pk)
        return instance
