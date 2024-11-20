from rest_framework import serializers
from pecoret.core.serializers import ValuedChoiceField, ProjectFilteredPrimaryKeyRelatedField
from .host import HostSerializer
from backend.models.assets.service import Protocol, Service, State


class ServiceSerializer(serializers.ModelSerializer):
    host = ProjectFilteredPrimaryKeyRelatedField(serializer=HostSerializer)
    protocol = ValuedChoiceField(choices=Protocol.choices)
    state = ValuedChoiceField(choices=State.choices, allow_null=True, default=None)

    def validate(self, data):
        assert data["protocol"] in ["TCP", "UDP", Protocol.TCP.value, Protocol.UDP.value]
        if data["port"] is None:
            raise serializers.ValidationError({"port": "This field is required"})
        if data.get("state") is None:
            raise serializers.ValidationError({"state": "This field is required"})
        return data

    class Meta:
        model = Service
        fields = [
            "pk", "host", "date_created", "date_updated", "name", "protocol",
            "port", "product", "state", "display_name"
        ]


class MinimalServiceSerializer(ServiceSerializer):
    class Meta:
        model = Service
        fields = [
            "pk", "name", "protocol", "port", "product", "state", "display_name"
        ]
