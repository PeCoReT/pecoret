from rest_framework import serializers

from attack_surface.models.finding import Finding, ProgressStatus, Severity
from attack_surface.serializers.program import ProgramSerializer
from backend.api.serializers.cwe import CWEMinimalSerializer
from backend.api.serializers.user import MinimalUserSerializer
from pecoret.core.serializers import PrimaryKeyRelatedField, ValuedChoiceField


class FindingCreateSerializer(serializers.ModelSerializer):
    program = PrimaryKeyRelatedField(serializer=ProgramSerializer)

    class Meta:
        model = Finding
        fields = ['title', 'pk', 'program']


class FindingSerializer(serializers.ModelSerializer):
    cwe_ids = PrimaryKeyRelatedField(serializer=CWEMinimalSerializer, many=True, required=False)
    status = ValuedChoiceField(choices=ProgressStatus.choices, required=False)
    severity = ValuedChoiceField(choices=Severity.choices, required=False)
    program = PrimaryKeyRelatedField(serializer=ProgramSerializer)
    created_by_user = PrimaryKeyRelatedField(serializer=MinimalUserSerializer, read_only=True)
    edited_by_user = PrimaryKeyRelatedField(serializer=MinimalUserSerializer, read_only=True)

    class Meta:
        model = Finding
        fields = [
            'pk', 'title', 'program', 'description', 'recommendation', 'created_by_user', 'edited_by_user',
            'severity', 'cwe_ids', 'internal_notes', 'cvss_score', 'exploitation_details', 'status',
            'date_created', 'date_updated'
        ]
        read_only_fields = ['created_by_user', 'edited_by_user']
