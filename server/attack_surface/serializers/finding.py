from rest_framework import serializers

from attack_surface.models.finding import Finding, ProgressStatus, Severity
from attack_surface.serializers.program import ProgramSerializer
from backend.api.serializers.cwe import CWEMinimalSerializer
from backend.api.serializers.user import MinimalUserSerializer
from pecoret.core.serializers import PrimaryKeyRelatedField, ValuedChoiceField
from pecoret.core.utils.markdown import markdown2html


class FindingCreateSerializer(serializers.ModelSerializer):
    program = PrimaryKeyRelatedField(serializer=ProgramSerializer)

    class Meta:
        model = Finding
        fields = ["title", "pk", "program"]


class FindingSerializer(serializers.ModelSerializer):
    cwe_ids = PrimaryKeyRelatedField(
        serializer=CWEMinimalSerializer, many=True, required=False
    )
    status = ValuedChoiceField(choices=ProgressStatus.choices, required=False)
    severity = ValuedChoiceField(choices=Severity.choices, required=False)
    program = PrimaryKeyRelatedField(serializer=ProgramSerializer)
    created_by_user = PrimaryKeyRelatedField(
        serializer=MinimalUserSerializer, read_only=True
    )
    edited_by_user = PrimaryKeyRelatedField(
        serializer=MinimalUserSerializer, read_only=True
    )
    locked_by = PrimaryKeyRelatedField(serializer=MinimalUserSerializer, read_only=True)
    description_html = serializers.SerializerMethodField()
    recommendation_html = serializers.SerializerMethodField()
    exploitation_details_html = serializers.SerializerMethodField()
    internal_notes_html = serializers.SerializerMethodField()

    def get_description_html(self, obj):
        # users that are allowed to read here are pentester group users only, so not limited
        return markdown2html(obj.description, limited=False, safe=False)

    def get_recommendation_html(self, obj):
        return markdown2html(obj.recommendation, limited=False, safe=False)

    def get_exploitation_details_html(self, obj):
        return markdown2html(obj.exploitation_details, limited=False, safe=False)

    def get_internal_notes_html(self, obj):
        return markdown2html(obj.internal_notes, limited=False, safe=False)

    class Meta:
        model = Finding
        fields = [
            "pk",
            "title",
            "program",
            "description",
            "recommendation",
            "created_by_user",
            "edited_by_user",
            "severity",
            "cwe_ids",
            "internal_notes",
            "cvss_score",
            "exploitation_details",
            "status",
            "date_created",
            "date_updated",
            "is_locked",
            "locked_by",
            "exploitation_details_html",
            "internal_notes_html",
            "recommendation_html",
            "description_html",
        ]
        read_only_fields = ["created_by_user", "edited_by_user", "locked_by"]
