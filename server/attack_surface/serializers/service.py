from django_q.tasks import async_task
from rest_framework import serializers

from attack_surface import tasks
from attack_surface.serializers.target import MinimalTargetSerializer
from attack_surface.models.service import Service, PortStatus, Protocol
from backend.api.serializers.technology import FlatTechnologySerializer
from pecoret.core.serializers import PrimaryKeyRelatedField, ValuedChoiceField
from .tag import TagSerializer


class ServiceSerializer(serializers.ModelSerializer):
    target = PrimaryKeyRelatedField(serializer=MinimalTargetSerializer)
    technologies = PrimaryKeyRelatedField(serializer=FlatTechnologySerializer, many=True, required=False)
    tags = PrimaryKeyRelatedField(serializer=TagSerializer, many=True, required=False)
    port_status = ValuedChoiceField(choices=PortStatus.choices, required=False)
    protocol = ValuedChoiceField(choices=Protocol.choices)

    class Meta:
        model = Service
        fields = [
            'pk', 'date_created', 'date_updated', 'target', 'uses_encryption',
            'banner', 'technologies', 'tags', 'cert_san', 'cert_expiry',
            'cert_subject', 'cert_valid_from', 'cert_expiry', 'cert_fingerprint',
            'cert_public_key_info', 'scheme', 'display_name', 'service_name', 'port_status', 'port_number', 'protocol'
        ]

    def create(self, validated_data):
        instance = super().create(validated_data)
        async_task(tasks.sync_implicit_techs_url, instance.pk)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        async_task(tasks.sync_implicit_techs_url, instance.pk)
        return instance
