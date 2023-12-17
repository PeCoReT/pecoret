from rest_framework import serializers
from pecoret.core.serializers import AssetGenericRelatedField, PrimaryKeyRelatedField
from checklists.models import Checklist, AssetChecklist
from checklists.serializers.category import CategorySerializer
from backend.serializers.assets.web_application import WebApplicationSerializer
from backend.serializers.assets.host import HostSerializer
from backend.serializers.assets.service import MinimalServiceSerializer
from backend.serializers.assets.mobile_application import MobileApplicationSerializer
from backend.serializers.assets.thick_client import ThickClientSerializer
from backend.serializers.assets.generic import GenericAssetSerializer
from backend.models import Host, Service, MobileApplication, WebApplication, ThickClient, GenericAsset


class ChecklistIdField(serializers.Field):
    default_error_messages = {"invalid_id": "Invalid checklist_id"}

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        if Checklist.objects.filter(checklist_id=data).exists():
            return data
        self.fail("invalid_id")


class ChecklistSerializer(serializers.ModelSerializer):
    categories = PrimaryKeyRelatedField(serializer=CategorySerializer, many=True)

    class Meta:
        model = Checklist
        fields = [
            "pk",
            "name",
            "checklist_id",
            'categories'
        ]


class AssetChecklistSerializer(ChecklistSerializer):
    component = AssetGenericRelatedField({
        WebApplication: WebApplicationSerializer(),
        Host: HostSerializer(),
        Service: MinimalServiceSerializer(),
        MobileApplication: MobileApplicationSerializer(),
        ThickClient: ThickClientSerializer(),
        GenericAsset: GenericAssetSerializer()
    })

    class Meta:
        model = AssetChecklist
        fields = ChecklistSerializer.Meta.fields + ["component"]


class AssetChecklistCreateSerializer(AssetChecklistSerializer):
    checklist_id = ChecklistIdField()

    class Meta:
        model = AssetChecklist
        fields = ["checklist_id", "component"]

    def create(self, validated_data):
        return AssetChecklist.objects.create_from_checklist(**validated_data)
