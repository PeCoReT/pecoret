from rest_framework import serializers
from backend.api.serializers.technology import TechnologySerializer
from backend.models import Asset, CustomFieldAsset, CustomFieldAssetValue
from backend.models.asset import Environment, AssetAccessibility
from core.custom_fields.serializers import CustomFieldRelatedSerializer, CustomFieldSerializer
from pecoret.core.serializers import ValuedChoiceField, PrimaryKeyRelatedField
from .asset_type import AssetTypeSerializer


class CustomFieldAssetSerializer(CustomFieldSerializer):
    class Meta:
        model = CustomFieldAsset
        fields = CustomFieldSerializer.Meta.fields


class CustomFieldAssetValueSerializer(serializers.ModelSerializer):
    field = CustomFieldAssetSerializer(read_only=True)

    class Meta:
        model = CustomFieldAssetValue
        fields = ['pk', 'field', 'value']


class AssetSerializer(CustomFieldRelatedSerializer):
    environment = ValuedChoiceField(choices=Environment.choices, required=False)
    accessible = ValuedChoiceField(choices=AssetAccessibility.choices, required=False)
    technologies = PrimaryKeyRelatedField(serializer=TechnologySerializer, many=True, required=False)
    asset_type = PrimaryKeyRelatedField(serializer=AssetTypeSerializer, required=True)

    class Meta:
        model = Asset
        fields = [
            "pk",
            "name",
            "date_updated",
            "date_created",
            "accessible",
            "description",
            "environment",
            "technologies",
            "asset_type"
        ]

    def get_custom_field_class(self):
        return CustomFieldAsset

    def get_custom_field_value_class(self):
        return CustomFieldAssetValue

    def get_custom_field_value(self, instance, field):
        try:
            value = CustomFieldAssetValue.objects.for_asset(instance).get(field=field)
        except CustomFieldAssetValue.DoesNotExist:
            value = None
        return value

    def get_value_serializer_class(self):
        return CustomFieldAssetValueSerializer
