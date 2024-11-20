from rest_framework import serializers
from .base import BaseAssetSerializer
from backend.models import Host


class HostSerializer(BaseAssetSerializer):
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Host
        fields = BaseAssetSerializer.Meta.fields + [
            "ip", "dns", "name", "operating_system"
        ]
