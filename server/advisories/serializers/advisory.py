from rest_framework import serializers
from backend.models.advisory import (
    Advisory, Severity, AdvisoryStatusChoices, VisibilityChoices, VulnerabilityStatusChoices
)
from backend.serializers.report_templates import ReportTemplateMinimalSerializer
from backend.serializers.user import MinimalUserSerializer
from backend.serializers.vulnerability import VulnerabilityTemplateSerializer
from pecoret.core.serializers import (
    ValuedChoiceField, VulnerabilityTemplateIdField, ActiveReportTemplateSerializerField
)


class BaseAdvisorySerializer(serializers.ModelSerializer):
    severity = ValuedChoiceField(choices=Severity.choices)
    vulnerability_id = serializers.ReadOnlyField()
    user = MinimalUserSerializer(read_only=True)

    class Meta:
        model = Advisory
        fields = [
            "pk", "user",
            "product", "affected_versions", "severity",
            "vendor_url", "vendor_name", "description", "internal_name",
            "recommendation", "date_created", "date_updated",
            "custom_report_title", "hide_advisory_id_in_report",
            "proof_text"
        ]
        read_only_fields = [
            "pk", "user"
        ]


class AdvisoryCreateSerializer(BaseAdvisorySerializer):
    vulnerability_id = VulnerabilityTemplateIdField(source="vulnerability_key")
    report_template = ActiveReportTemplateSerializerField(required=False, serializer=ReportTemplateMinimalSerializer)

    class Meta(BaseAdvisorySerializer.Meta):
        fields = BaseAdvisorySerializer.Meta.fields + ["vulnerability_id", "report_template"]

    def create(self, validated_data):
        return Advisory.objects.create_from_template(**validated_data)


class AdvisorySerializer(BaseAdvisorySerializer):
    vulnerability = VulnerabilityTemplateSerializer()
    status = ValuedChoiceField(choices=AdvisoryStatusChoices.choices)
    visibility = ValuedChoiceField(choices=VisibilityChoices.choices)
    vulnerability_status = ValuedChoiceField(choices=VulnerabilityStatusChoices.choices)
    report_template = ActiveReportTemplateSerializerField(required=False, serializer=ReportTemplateMinimalSerializer)

    class Meta(BaseAdvisorySerializer.Meta):
        fields = BaseAdvisorySerializer.Meta.fields + ["status", "vulnerability", "cve_id",
                                                       "report_template", "fixed_version",
                                                       "vulnerability_status", "visibility", "date_planned_disclosure"]


class AdvisoryUpdateSerializer(AdvisorySerializer):
    vulnerability = VulnerabilityTemplateSerializer(read_only=True)
    vulnerability_id = VulnerabilityTemplateIdField(source="vulnerability_key")
    report_template = ActiveReportTemplateSerializerField(required=False, serializer=ReportTemplateMinimalSerializer)

    class Meta(AdvisorySerializer.Meta):
        fields = AdvisorySerializer.Meta.fields + ["vulnerability_id", "report_template"]


class AdvisoryDownloadSerializer(serializers.Serializer):
    report_template = ActiveReportTemplateSerializerField(required=False, serializer=ReportTemplateMinimalSerializer)

    class Meta:
        fields = [
            "template"
        ]
