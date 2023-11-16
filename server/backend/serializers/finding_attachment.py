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
        repr = super().to_representation(instance)
        attachment_url = reverse("backend:findings:attachment-preview", kwargs={
            'project': instance.finding.project.pk,
            'finding': instance.finding.pk, 'pk': instance.pk})
        repr["image"] = self.context["request"].build_absolute_uri(attachment_url)
        repr["name"] = instance.name
        return repr
