from rest_framework import serializers
from checklists.models import Item, AssetItem
from checklists.models.item import ItemStatus
from checklists.serializers.category import CategorySerializer
from pecoret.core.serializers import ValuedChoiceField, PrimaryKeyRelatedField


class BaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            "pk", "name", "item_id", "description", "date_created", "date_updated"
        ]


class AssetItemSerializer(BaseItemSerializer):
    status = ValuedChoiceField(choices=ItemStatus.choices)

    class Meta:
        model = AssetItem
        fields = BaseItemSerializer.Meta.fields + ["status"]


class AssetItemUpdateSerializer(AssetItemSerializer):
    class Meta:
        model = AssetItem
        fields = ["status"]


class ItemSerializer(BaseItemSerializer):
    category = PrimaryKeyRelatedField(serializer=CategorySerializer)
    class Meta:
        model = Item
        fields = BaseItemSerializer.Meta.fields + ['category']
