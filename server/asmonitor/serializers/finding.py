from rest_framework import serializers
from pecoret.core.serializers import PrimaryKeyRelatedField, ValuedChoiceField
from asmonitor.models.finding import Finding, Severity, Status
from backend.serializers.cwe import CWEMinimalSerializer
from .target import TargetSerializer
from .program import ProgramSerializer


class FindingSerializer(serializers.ModelSerializer):
    target = PrimaryKeyRelatedField(serializer=TargetSerializer)
    severity = ValuedChoiceField(choices=Severity.choices)
    status = ValuedChoiceField(choices=Status.choices, required=False)
    cwe = PrimaryKeyRelatedField(serializer=CWEMinimalSerializer, required=False)

    class Meta:
        model = Finding
        fields = [
            'pk', 'name', 'severity', 'cwe', 'proof_text', 'target', 'status'
        ]


class GlobalFindingSerializer(FindingSerializer):
    program = PrimaryKeyRelatedField(serializer=ProgramSerializer)

    class Meta:
        model = Finding
        fields = FindingSerializer.Meta.fields + ['program']
