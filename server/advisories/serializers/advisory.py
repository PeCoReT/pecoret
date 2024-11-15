from rest_framework import serializers
from advisories.fields import LabelField
from advisories.models.advisory import (
    Advisory, Severity, AdvisoryStatusChoices, VulnerabilityStatusChoices
)
from advisories import fields
from backend.api.serializers.user import MinimalUserSerializer
from backend.api.serializers.vulnerability import VulnerabilityTemplateSerializer
from backend.api.serializers.technology import TechnologySerializer
from pecoret.core.serializers import (
    ValuedChoiceField, VulnerabilityTemplateIdField,
    PrimaryKeyRelatedField
)
from .label import LabelSerializer


class BaseAdvisorySerializer(serializers.ModelSerializer):
    severity = ValuedChoiceField(choices=Severity.choices)
    vulnerability_id = serializers.ReadOnlyField()
    user = MinimalUserSerializer(read_only=True)
    labels = LabelField(serializer=LabelSerializer, many=True, read_only=True)
    technology = PrimaryKeyRelatedField(serializer=TechnologySerializer)
    advisory_id = serializers.CharField(read_only=True)

    class Meta:
        model = Advisory
        fields = [
            "pk", "user", "affected_versions", "severity",
            "description", "advisory_id", "technology",
            "recommendation", "date_created", "date_updated",
            "custom_report_title", "hide_advisory_id_in_report",
            "proof_text", "labels", "researchers", "report_template",
            "title"
        ]
        read_only_fields = [
            "pk", "user"
        ]


class AdvisoryCreateSerializer(BaseAdvisorySerializer):
    vulnerability_id = VulnerabilityTemplateIdField(source="vulnerability_key")

    class Meta(BaseAdvisorySerializer.Meta):
        fields = BaseAdvisorySerializer.Meta.fields + ["vulnerability_id", "report_template"]

    def create(self, validated_data):
        return Advisory.objects.create_from_template(**validated_data)


class AdvisorySerializer(BaseAdvisorySerializer):
    vulnerability = VulnerabilityTemplateSerializer()
    status = ValuedChoiceField(choices=AdvisoryStatusChoices.choices)
    vulnerability_status = ValuedChoiceField(choices=VulnerabilityStatusChoices.choices)

    class Meta(BaseAdvisorySerializer.Meta):
        fields = BaseAdvisorySerializer.Meta.fields + ["status", "vulnerability", "cve_id",
                                                       "report_template", "fixed_version",
                                                       "vulnerability_status", "date_planned_disclosure"]


class AdvisoryUpdateSerializer(AdvisorySerializer):
    vulnerability = VulnerabilityTemplateSerializer(read_only=True)
    vulnerability_id = VulnerabilityTemplateIdField(source="vulnerability_key")
    labels = fields.LabelField(serializer=LabelSerializer, many=True)

    class Meta(AdvisorySerializer.Meta):
        fields = AdvisorySerializer.Meta.fields + ["vulnerability_id", "report_template", "labels"]


class AdvisoryDownloadSerializer(serializers.Serializer):

    class Meta:
        fields = [
            "template"
        ]
