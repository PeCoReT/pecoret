from rest_framework import serializers

from backend.api.serializers.technology import TechnologySerializer
from backend.models import Asset, CustomFieldAsset, CustomFieldAssetValue
from backend.models.asset import Environment, AssetAccessibility
from core.custom_fields.serializers import CustomFieldSerializer
from pecoret.core.serializers import ValuedChoiceField, PrimaryKeyRelatedField
from .asset_type import AssetTypeSerializer


class CustomFieldAssetSerializer(CustomFieldSerializer):
    class Meta:
        model = CustomFieldAsset
        fields = CustomFieldSerializer.Meta.fields


class BaseCustomFieldAssetValueSerializer(serializers.ModelSerializer):
    field = CustomFieldAssetSerializer(read_only=True)

    class Meta:
        model = CustomFieldAssetValue
        fields = ['pk', 'field', 'value']


class CustomFieldAssetValueSerializer(serializers.Serializer):

    def to_representation(self, instance):
        serializer = BaseCustomFieldAssetValueSerializer(
            CustomFieldAssetValue.objects.for_asset(instance),
            many=True,
            read_only=True
        )
        return serializer.data


class AssetSerializer(serializers.ModelSerializer):
    environment = ValuedChoiceField(choices=Environment.choices, required=False)
    accessible = ValuedChoiceField(choices=AssetAccessibility.choices, required=False)
    technologies = PrimaryKeyRelatedField(serializer=TechnologySerializer, many=True, required=False)
    asset_type = PrimaryKeyRelatedField(serializer=AssetTypeSerializer, required=True)
    custom_fields = CustomFieldAssetValueSerializer(source='*', read_only=True)

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
            "asset_type",
            "custom_fields",
        ]

    def to_internal_value(self, data):
        if not data.get('asset_type'):
            asset_type = self.instance.asset_type
        else:
            asset_type = data['asset_type']
        for field in CustomFieldAsset.objects.for_asset_type(asset_type):
            self.fields[f'custom_{field.name}'] = field.get_serializer_field()
            self.fields[f'custom_{field.name}'].write_only = True
        return super().to_internal_value(data)

    def to_representation(self, value):
        for key, field_value in self.fields.items():
            if key.startswith('custom_'):
                CustomFieldAssetValueSerializer(instance=getattr(value, key, None))
        representation = super().to_representation(value)
        return representation

    def create(self, validated_data):
        custom_fields = {}
        for field in CustomFieldAsset.objects.for_asset_type(validated_data['asset_type']):
            custom_fields[field.pk] = validated_data.pop(f'custom_{field.name}', None)
        instance = super().create(validated_data)
        for field_pk, value in custom_fields.items():
            try:
                # get custom field if one exists and populate it
                custom_field = CustomFieldAsset.objects.get(pk=field_pk)
            except CustomFieldAsset.DoesNotExist:
                # if no custom asset field exists, continue
                continue
            CustomFieldAssetValue.objects.create(asset=instance, field=custom_field, value=value)
            setattr(instance, f'custom_{custom_field.name}', value)
        return instance

    def update(self, instance, validated_data):
        custom_fields = {}
        asset_type_changed = False
        # we have a PATCH and no change in asset type
        if not validated_data.get('asset_type'):
            asset_type = instance.asset_type
        else:
            asset_type = validated_data['asset_type']
            asset_type_changed = True
        for field in CustomFieldAsset.objects.for_asset_type(asset_type):
            if f'custom_{field.name}' in validated_data.keys():
                custom_fields[field.pk] = validated_data.pop(f'custom_{field.name}', None)
        instance = super().update(instance, validated_data)
        if asset_type_changed is True:
            instance.customfieldassetvalue_set.all().delete()
        for field_pk, value in custom_fields.items():
            try:
                custom_field = CustomFieldAsset.objects.get(pk=field_pk)
            except CustomFieldAsset.DoesNotExist:
                # if no custom asset field exists, continue
                continue
            CustomFieldAssetValue.objects.update_or_create(
                asset=instance, field=custom_field, defaults={"value": value})
            setattr(instance, f'custom_{custom_field.name}', value)
        return instance
