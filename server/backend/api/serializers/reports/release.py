from rest_framework import serializers
from backend.models.reports.report_release import ReportRelease, ReleaseType
from backend.api.serializers.django_q_task import DjangoQTaskSerializer
from pecoret.core.serializers import ValuedChoiceField


class ReportReleaseSerializer(serializers.ModelSerializer):
    release_type = ValuedChoiceField(choices=ReleaseType.choices)
    task = DjangoQTaskSerializer(read_only=True)

    class Meta:
        model = ReportRelease
        fields = [
            "pk", "date_created", "date_updated", "name", "release_type", "task",
            "task_id"
        ]
        read_only_fields = ["task_id"]
