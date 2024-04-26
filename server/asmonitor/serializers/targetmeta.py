from rest_framework import serializers
from asmonitor.models import TargetMeta


class TargetMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetMeta
        fields = [
            'pk', 'key', 'value', 'date_created', 'date_updated'
        ]
