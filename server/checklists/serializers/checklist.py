from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from backend.api.serializers.asset import AssetSerializer
from checklists.models import Checklist, AssetChecklist
from checklists.serializers.category import CategorySerializer
from pecoret.core.serializers import PrimaryKeyRelatedField, \
    ProjectFilteredPrimaryKeyRelatedField


@extend_schema_field(OpenApiTypes.STR)
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
    asset = ProjectFilteredPrimaryKeyRelatedField(serializer=AssetSerializer)

    class Meta:
        model = AssetChecklist
        fields = ChecklistSerializer.Meta.fields + ["asset"]


class AssetChecklistCreateSerializer(AssetChecklistSerializer):
    checklist_id = ChecklistIdField()

    class Meta:
        model = AssetChecklist
        fields = ["checklist_id", "asset"]

    def create(self, validated_data):
        return AssetChecklist.objects.create_from_checklist(**validated_data)
