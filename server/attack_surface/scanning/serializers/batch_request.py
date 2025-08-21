from rest_framework import serializers

from attack_surface.scanning.models.scan_batch import (
    StatusChoices,
    TriggerSource,
    ScanBatchRequest,
)
from attack_surface.scanning.serializers.scan_template import (
    ScanTemplateSerializer,
    MinimalScanTemplateSerializer,
)
from attack_surface.serializers.program import ProgramSerializer
from attack_surface.serializers.service import ServiceSerializer
from attack_surface.serializers.target import TargetSerializer
from attack_surface.serializers.url import URLSerializer
from pecoret.core.serializers import ValuedChoiceField, PrimaryKeyRelatedField


class ScanBatchRequestSerializer(serializers.ModelSerializer):
    scan_template = PrimaryKeyRelatedField(serializer=ScanTemplateSerializer)
    status = ValuedChoiceField(choices=StatusChoices.choices, required=False)
    programs = PrimaryKeyRelatedField(serializer=ProgramSerializer, many=True)
    targets = PrimaryKeyRelatedField(serializer=TargetSerializer, many=True)
    services = PrimaryKeyRelatedField(serializer=ServiceSerializer, many=True)
    urls = PrimaryKeyRelatedField(serializer=URLSerializer, many=True)
    scan_trigger_source = ValuedChoiceField(
        choices=TriggerSource.choices, required=False
    )

    class Meta:
        model = ScanBatchRequest
        fields = [
            "pk",
            "date_created",
            "date_updated",
            "scan_template",
            "targets",
            "services",
            "urls",
            "programs",
            "status",
            "batch_start_time",
            "batch_end_time",
            "triggered_by",
            "scan_trigger_source",
            "date_last_item_added",
            "is_discovery_scan",
            "notes",
            "raw_output",
            "errors",
        ]
        read_only_fields = ["raw_output", "errors"]


class ScanBatchFetchSerializer(serializers.ModelSerializer):
    scan_template = PrimaryKeyRelatedField(serializer=ScanTemplateSerializer)
    programs = PrimaryKeyRelatedField(serializer=ProgramSerializer, many=True)
    targets = serializers.SerializerMethodField()
    services = PrimaryKeyRelatedField(serializer=ServiceSerializer, many=True)
    urls = serializers.SerializerMethodField()

    def get_targets(self, obj):
        return [TargetSerializer(t).data for t in obj.targets.all().iterator()]

    def get_urls(self, obj):
        return [URLSerializer(s).data for s in obj.urls.all().iterator()]

    class Meta:
        model = ScanBatchRequest
        fields = ["pk", "scan_template", "targets", "urls", "services", "programs"]


class ScanBatchRequestUpdateSerializer(serializers.ModelSerializer):
    status = ValuedChoiceField(choices=StatusChoices.choices, required=False)

    class Meta:
        model = ScanBatchRequest
        fields = [
            "pk",
            "status",
            "batch_start_time",
            "batch_end_time",
            "raw_output",
            "errors",
        ]


class ScanBatchRequestListSerializer(serializers.ModelSerializer):
    status = ValuedChoiceField(choices=StatusChoices.choices)
    scan_template = PrimaryKeyRelatedField(serializer=MinimalScanTemplateSerializer)

    class Meta:
        model = ScanBatchRequest
        fields = [
            "pk",
            "date_created",
            "date_updated",
            "scan_template",
            "status",
            "batch_start_time",
            "batch_end_time",
        ]
