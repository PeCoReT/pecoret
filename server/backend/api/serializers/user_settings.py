from rest_framework import serializers
from backend.models import UserSettings


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = [
            "notify_before_disclosure_mail",
            "notify_critical_findings"
        ]
