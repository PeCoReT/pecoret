from rest_framework import serializers

from backend.models import User
from backend.models.reports.report import Report
from backend.api.serializers.user import MinimalUserSerializer
from pecoret.core.serializers import ReportAuthorRelatedField


class ReportSerializer(serializers.ModelSerializer):
    author = ReportAuthorRelatedField(
        serializer=MinimalUserSerializer, queryset=User.objects.all(),
        required=False, allow_null=True, allow_empty=True
    )

    class Meta:
        fields = [
            "pk",
            "date_created",
            "date_updated",
            "name",
            "title",
            "template",
            "author",
            "recommendation",
            "evaluation",
        ]
        model = Report
