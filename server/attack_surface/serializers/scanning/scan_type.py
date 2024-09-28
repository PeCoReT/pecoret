from rest_framework import serializers

from attack_surface.models import ScanType


class ScanTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanType
        fields = [
            'pk', 'name', 'description', 'allowed_object_type', 'can_run_manually', 'conditions', 'priority', 'enabled'
        ]
