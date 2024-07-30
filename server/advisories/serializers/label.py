from rest_framework import serializers
from advisories.models.label import Label


class LabelSerializer(serializers.ModelSerializer):
    color_rgb = serializers.CharField(read_only=True)

    class Meta:
        model = Label
        fields = [
            "name", "description", "color", "pk",
            "color_rgb",
        ]
