from rest_framework import serializers
from checklists.models import Item, AssetItem
from checklists.models.item import ItemStatus
from pecoret.core.serializers import ValuedChoiceField


class BaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            "pk", "name", "item_id", "description"
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
    class Meta:
        model = Item
        fields = BaseItemSerializer.Meta.fields + ['category']
