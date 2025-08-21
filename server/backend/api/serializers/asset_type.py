from rest_framework import serializers

from backend.models import AssetType


class AssetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetType
        fields = ['pk', 'name', 'description', 'date_created', 'date_updated']
