from django.urls import reverse
from rest_framework import serializers

from backend.models.finding_attachment import FindingImageAttachment


class FindingImageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FindingImageAttachment
        fields = [
            "pk", "date_created", "date_updated",
            "image"
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        attachment_url = reverse("api:backend:findings:attachment-preview", kwargs={
            'project': instance.finding.project.pk,
            'finding': instance.finding.pk, 'pk': instance.pk})
        rep["image"] = self.context["request"].build_absolute_uri(attachment_url)
        rep["name"] = instance.name
        return rep
