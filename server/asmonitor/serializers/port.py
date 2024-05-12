from rest_framework import serializers
from pecoret.core.serializers import ValuedChoiceField
from asmonitor.models.port import Port, Protocol


class PortSerializer(serializers.ModelSerializer):
    protocol = ValuedChoiceField(choices=Protocol.choices)

    class Meta:
        model = Port
        fields = [
            'pk', 'port', 'banner', 'service', 'date_created', 'date_updated', 'protocol'
        ]
