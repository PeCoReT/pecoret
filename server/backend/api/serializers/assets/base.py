from rest_framework import serializers
from pecoret.core.serializers import ValuedChoiceField, PrimaryKeyRelatedField
from backend.api.serializers.technology import TechnologySerializer
from backend.models.assets.base import Environment, AssetAccessibility


class BaseAssetSerializer(serializers.ModelSerializer):
    environment = ValuedChoiceField(choices=Environment.choices, required=False)
    accessible = ValuedChoiceField(choices=AssetAccessibility.choices, required=False)
    technologies = PrimaryKeyRelatedField(serializer=TechnologySerializer, many=True, required=False)
    # added for spectacular explicitly
    value = serializers.CharField(read_only=True)
    asset_type = serializers.CharField(read_only=True)

    class Meta:
        fields = [
            "pk",
            "date_updated",
            "date_created",
            "accessible",
            "description",
            "environment",
            "display_name",
            "asset_type", "technologies", "value"
        ]
        read_only_fields = ["asset_type"]
