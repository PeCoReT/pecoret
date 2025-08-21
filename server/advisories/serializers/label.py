from rest_framework import serializers
from advisories.models.label import Label


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = [
            "name", "description", "color", "pk"
        ]
