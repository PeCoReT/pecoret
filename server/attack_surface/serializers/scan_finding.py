from rest_framework import serializers

from attack_surface.models.scan_finding import ScanFinding, ScanFindingStatus
from backend.models.finding import Severity
from pecoret.core.serializers import ValuedChoiceField
from pecoret.core.utils.markdown import markdown2html


class ScanFindingSerializer(serializers.ModelSerializer):
    severity = ValuedChoiceField(choices=Severity.choices)
    status = ValuedChoiceField(choices=ScanFindingStatus.choices, required=False)
    ignore_until = serializers.DateField(required=False, allow_null=True)
    result_html = serializers.SerializerMethodField()

    def get_result_html(self, obj):
        return markdown2html(obj.result, limited=True, safe=False)

    class Meta:
        model = ScanFinding
        fields = [
            "pk",
            "name",
            "comment",
            "date_created",
            "date_updated",
            "severity",
            "status",
            "affected_component",
            "false_positive",
            "full_output",
            "result",
            "result_html",
            "tool",
            "ignore_until",
        ]


class ScanFindingStatusUpdateSerializer(serializers.ModelSerializer):
    status = ValuedChoiceField(choices=ScanFindingStatus.choices)

    class Meta:
        model = ScanFinding
        fields = ["status", "comment", "false_positive", "ignore_until"]
