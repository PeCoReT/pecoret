from rest_framework import serializers

from backend.models import User
from backend.models.reports.report import Report
from backend.api.serializers.user import MinimalUserSerializer
from pecoret.core.serializers import ReportAuthorRelatedField


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
