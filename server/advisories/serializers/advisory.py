from rest_framework import serializers
from advisories.fields import LabelField
from advisories.models.advisory import (
    Advisory,
    Severity,
    AdvisoryStatusChoices,
    VulnerabilityStatusChoices,
)
from advisories import fields
from backend.api.serializers.user import MinimalUserSerializer
from backend.api.serializers.cwe import CWEMinimalSerializer
from backend.api.serializers.technology import TechnologySerializer
from pecoret.core.serializers import (
    ValuedChoiceField,
    PrimaryKeyRelatedField,
)
from pecoret.core.utils.markdown import markdown2html
from .label import LabelSerializer


class BaseAdvisorySerializer(serializers.ModelSerializer):
    severity = ValuedChoiceField(choices=Severity.choices)
    cwes = PrimaryKeyRelatedField(
        serializer=CWEMinimalSerializer, many=True, read_only=True
    )
    user = MinimalUserSerializer(read_only=True)
    labels = LabelField(serializer=LabelSerializer, many=True, read_only=True)
    technology = PrimaryKeyRelatedField(serializer=TechnologySerializer)
    advisory_id = serializers.CharField(read_only=True)
    description_html = serializers.SerializerMethodField()
    proof_html = serializers.SerializerMethodField()
    recommendation_html = serializers.SerializerMethodField()

    def get_description_html(self, obj):
        return markdown2html(obj.description)

    def get_proof_html(self, obj):
        return markdown2html(obj.proof_text)

    def get_recommendation_html(self, obj):
        return markdown2html(obj.recommendation)

    class Meta:
        model = Advisory
        fields = [
            "pk",
            "user",
            "affected_versions",
            "severity",
            "description",
            "description_html",
            "advisory_id",
            "technology",
            "recommendation",
            "recommendation_html",
            "proof_html",
            "date_created",
            "date_updated",
            "custom_report_title",
            "hide_advisory_id_in_report",
            "proof_text",
            "labels",
            "researchers",
            "report_template",
            "title",
            "cwes",
            "is_draft",
            "cvss_vector",
        ]
        read_only_fields = ["pk", "user", "cwes"]


class AdvisoryCreateSerializer(BaseAdvisorySerializer):
    cwes = PrimaryKeyRelatedField(serializer=CWEMinimalSerializer, many=True)

    class Meta(BaseAdvisorySerializer.Meta):
        fields = BaseAdvisorySerializer.Meta.fields + [
            "cwes",
            "report_template",
        ]

    def create(self, validated_data):
        return Advisory.objects.create_from_data(**validated_data)


class AdvisorySerializer(BaseAdvisorySerializer):
    status = ValuedChoiceField(choices=AdvisoryStatusChoices.choices)
    vulnerability_status = ValuedChoiceField(choices=VulnerabilityStatusChoices.choices)

    class Meta(BaseAdvisorySerializer.Meta):
        fields = BaseAdvisorySerializer.Meta.fields + [
            "status",
            "cve_id",
            "report_template",
            "fixed_version",
            "vulnerability_status",
            "date_planned_disclosure",
        ]


class AdvisoryUpdateSerializer(AdvisorySerializer):
    cwes = PrimaryKeyRelatedField(serializer=CWEMinimalSerializer, many=True)
    labels = fields.LabelField(serializer=LabelSerializer, many=True)

    class Meta(AdvisorySerializer.Meta):
        fields = AdvisorySerializer.Meta.fields + [
            "report_template",
            "labels",
        ]


class AdvisoryDownloadSerializer(serializers.Serializer):

    class Meta:
        fields = ["template"]
