from rest_framework import serializers
from advisories.models.advisory_comment import AdvisoryComment
from backend.api.serializers.user import MinimalUserSerializer


class AdvisoryCommentSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer(read_only=True)
    user_edit = MinimalUserSerializer(read_only=True)

    class Meta:
        model = AdvisoryComment
        fields = ["pk", "comment", "user", "user_edit", "date_created", "date_updated"]
