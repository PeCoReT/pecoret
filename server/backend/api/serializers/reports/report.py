from rest_framework import serializers

from backend.models.reports.report import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "pk",
            "date_created",
            "date_updated",
            "name",
            "title",
            "template",
            "recommendation",
            "evaluation",
        ]
        model = Report
