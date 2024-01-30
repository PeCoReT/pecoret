from rest_framework import serializers
from advisories.models.attachment import ImageAttachment


class ImageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageAttachment
        fields = [
            "pk", "date_created", "date_updated",
            "image"
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["image"] = self.context["request"].build_absolute_uri(instance.get_preview_url())
        rep["name"] = instance.name
        return rep
