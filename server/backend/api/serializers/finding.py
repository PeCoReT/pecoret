from rest_framework import serializers

from backend.api.serializers.fields.technology import TechnologyField
from backend.models import ProjectVulnerability
from backend.models.finding import Finding, Severity, FindingStatus
from pecoret.core.serializers import (
    ValuedChoiceField,
    ProjectVulnerabilityIdField,
    ProjectFilteredPrimaryKeyRelatedField
)
from .account import AccountSerializer
from .asset import AssetSerializer
from .vulnerability import ProjectVulnerabilitySerializer


class FindingSerializer(serializers.ModelSerializer):
    vulnerability = ProjectVulnerabilitySerializer(
        ProjectVulnerability.objects.all(), read_only=True
    )
    severity = ValuedChoiceField(choices=Severity.choices)
    status = ValuedChoiceField(choices=FindingStatus.choices)
    internal_id = serializers.CharField(read_only=True)
    user_account = ProjectFilteredPrimaryKeyRelatedField(
        required=False, allow_empty=True, allow_null=True, serializer=AccountSerializer
    )
    authentication_required = serializers.BooleanField(read_only=True)
    asset = ProjectFilteredPrimaryKeyRelatedField(required=True, serializer=AssetSerializer)

    class Meta:
        model = Finding
        fields = [
            "pk",
            "date_created",
            "date_updated",
            "vulnerability",
            "internal_id",
            "user_account",
            "recommendation",
            "severity",
            "status",
            "imported",
            "name",
            "cvss_score_40",
            "cvss_score_31",
            "unique_id",
            "finding_date",
            "authentication_required",
            "needs_review",
            "retest_results",
            "date_retest",
            "exclude_from_report",
            "asset",
            "proof_text",
            "entrypoint"
        ]


class FindingCopySerializer(FindingSerializer):
    class Meta:
        model = Finding
        fields = ["name"]
        read_only_fields = [
            "pk",
            "date_created",
            "date_updated",
            "vulnerability",
            "internal_id",
            "recommendation",
            "severity",
            "status",
            "needs_review",
            "asset",
            "vulnerability_id",
        ]


class FindingCreateSerializer(FindingSerializer):
    vulnerability_id = ProjectVulnerabilityIdField(source="vuln_key")
    severity = ValuedChoiceField(choices=Severity.choices, required=False)

    def create(self, validated_data):
        return Finding.objects.create_from_template(**validated_data)

    class Meta(FindingSerializer.Meta):
        fields = FindingSerializer.Meta.fields + ["vulnerability_id"]


class FindingAsAdvisorySerializer(serializers.Serializer):
    technology = TechnologyField()
    affected_versions = serializers.CharField()
