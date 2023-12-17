from rest_framework import serializers
from pecoret.core.serializers import PrimaryKeyRelatedField
from checklists.models import Category, AssetCategory
from .item import ItemSerializer, AssetItemSerializer


class CategorySerializer(serializers.ModelSerializer):
    items = PrimaryKeyRelatedField(many=True, read_only=True, serializer=ItemSerializer, source='item_set')

    class Meta:
        model = Category
        fields = ["pk", "name", "summary", "category_id", "items"]


class AssetCategorySerializer(CategorySerializer):
    items = AssetItemSerializer(many=True, read_only=True, source="assetitem_set")

    class Meta:
        model = AssetCategory
        fields = CategorySerializer.Meta.fields
