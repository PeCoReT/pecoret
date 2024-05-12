from rest_framework import serializers
from asmonitor.models import Hostname


class HostnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostname
        fields = [
            'pk', 'name', 'date_created', 'date_updated'
        ]
