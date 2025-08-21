from rest_framework import serializers
from checklists.models import Category, AssetCategory


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["pk", "name", "summary", "category_id"]


class AssetCategorySerializer(CategorySerializer):

    class Meta:
        model = AssetCategory
        fields = CategorySerializer.Meta.fields
