from rest_framework import serializers
from checklists.models import AssetCategory
from checklists.serializers.item import AssetItemSerializer


class AssetCategorySerializer(serializers.ModelSerializer):
    items = AssetItemSerializer(many=True, read_only=True, source="assetitem_set")

    class Meta:
        model = AssetCategory
        fields = ["pk", "name", "summary", "category_id", "items"]
