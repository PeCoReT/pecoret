from rest_framework import serializers
from backend.models import PinnedProject


class PinnedProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PinnedProject
        exclude = ["project", "user"]
