from rest_framework import serializers
from backend.models.report_templates import ReportTemplate, ReportTemplateStatus
from pecoret.core.serializers import ValuedChoiceField


class ReportTemplateMinimalSerializer(serializers.ModelSerializer):
    """a report template serializer that does not expose path information
    """
    status = ValuedChoiceField(choices=ReportTemplateStatus.choices)

    class Meta:
        model = ReportTemplate
        fields = ["pk", "status", "name"]


class ReportTemplateSerializer(ReportTemplateMinimalSerializer):
    class Meta:
        model = ReportTemplate
        fields = ReportTemplateMinimalSerializer.Meta.fields + [
            "date_created",
            "date_updated",
            "package",
        ]
