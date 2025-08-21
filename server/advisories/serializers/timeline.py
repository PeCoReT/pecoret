from rest_framework import serializers
from advisories.models.advisory_timeline import AdvisoryTimeline


class AdvisoryTimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvisoryTimeline
        fields = ["text", "date", "pk"]
