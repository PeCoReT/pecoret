from rest_framework import serializers

from backend.models.reports.change_history import ChangeHistory


class ChangeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeHistory
        fields = [
            "pk",
            "date_created",
            "date_updated",
            "change",
            "date",
            "version",
        ]
