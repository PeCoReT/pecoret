from rest_framework import serializers
from pecoret.core.serializers import ReportAuthorRelatedField
from backend.api.serializers.user import MinimalUserSerializer
from backend.models import User
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
