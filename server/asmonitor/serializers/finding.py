from rest_framework import serializers
from pecoret.core.serializers import PrimaryKeyRelatedField, ValuedChoiceField
from asmonitor.models.finding import Finding, Severity, Status
from backend.serializers.cwe import CWEMinimalSerializer
from .host import HostSerializer
from .program import ProgramSerializer
from .tag import TagSerializer


class FindingSerializer(serializers.ModelSerializer):
    host = PrimaryKeyRelatedField(serializer=HostSerializer)
    severity = ValuedChoiceField(choices=Severity.choices)
    status = ValuedChoiceField(choices=Status.choices, required=False)
    cwe = PrimaryKeyRelatedField(serializer=CWEMinimalSerializer, required=False, allow_null=True)
    tags = PrimaryKeyRelatedField(serializer=TagSerializer, many=True, required=False)

    class Meta:
        model = Finding
        fields = [
            'pk', 'name', 'severity', 'cwe', 'proof_text', 'host', 'status', 'tags'
        ]


class GlobalFindingSerializer(FindingSerializer):
    program = PrimaryKeyRelatedField(serializer=ProgramSerializer)

    class Meta:
        model = Finding
        fields = FindingSerializer.Meta.fields + ['program']
