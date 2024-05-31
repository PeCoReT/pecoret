from rest_framework import serializers
from pecoret.core.serializers import PrimaryKeyRelatedField, ValuedChoiceField
from attack_surface.models.scan_finding import ScanFinding, ScanFindingStatus
from attack_surface.serializers.program import ProgramSerializer
from backend.models.finding import Severity


class ScanFindingSerializer(serializers.ModelSerializer):
    severity = ValuedChoiceField(choices=Severity.choices)
    status = ValuedChoiceField(choices=ScanFindingStatus.choices, required=False)
    program = PrimaryKeyRelatedField(serializer=ProgramSerializer)

    class Meta:
        model = ScanFinding
        fields = [
            'pk', 'name', 'comment', 'date_created', 'date_updated', 'severity', 'status', 'program',
            'affected_component', 'false_positive', 'full_output', 'result', 'tool'
        ]
