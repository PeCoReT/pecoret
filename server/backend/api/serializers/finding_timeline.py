from rest_framework import serializers
from backend.models import FindingTimeline
from backend.api.serializers.user import BaseUserSerializer


class FindingTimelineSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = FindingTimeline
        fields = ["user", "pk", "text", "title", "date_created"]
