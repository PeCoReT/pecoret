from django_q.tasks import async_task
from rest_framework import serializers

from attack_surface import tasks
from attack_surface.models import Service
from attack_surface.serializers.port import PortSerializer
from attack_surface.serializers.target import MinimalTargetSerializer
from backend.serializers.technology import FlatTechnologySerializer
from pecoret.core.serializers import PrimaryKeyRelatedField
from .tag import TagSerializer


class ServiceSerializer(serializers.ModelSerializer):
    port = PrimaryKeyRelatedField(serializer=PortSerializer)
    target = PrimaryKeyRelatedField(serializer=MinimalTargetSerializer)
    technologies = PrimaryKeyRelatedField(serializer=FlatTechnologySerializer, many=True, required=False)
    tags = PrimaryKeyRelatedField(serializer=TagSerializer, many=True, required=False)

    class Meta:
        model = Service
        fields = [
            'pk', 'date_created', 'date_updated', 'port', 'target',
            'banner', 'technologies', 'tags', 'cert_san', 'cert_expiry',
            'cert_subject', 'cert_valid_from', 'cert_expiry', 'cert_fingerprint',
            'cert_public_key_info', 'scheme', 'display_name'
        ]

    def create(self, validated_data):
        instance = super().create(validated_data)
        async_task(tasks.sync_implicit_techs_url, instance.pk)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        async_task(tasks.sync_implicit_techs_url, instance.pk)
        return instance
