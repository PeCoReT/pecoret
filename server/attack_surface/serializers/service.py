from rest_framework import serializers
from attack_surface.models.service import Service, PortStatus, Protocol
from attack_surface.serializers.target import MinimalTargetSerializer
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

    def validate(self, data):
        banner = data.get('banner')
        if banner:
            # when a banner contains null bytes, strip it
            banner = data['banner'].replace(r"\x00", "")
            try:
                banner = banner.encode().decode('unicode_escape', errors='ignore')
            except UnicodeEncodeError:
                pass
            data['banner'] = banner
        return super().validate(data)
