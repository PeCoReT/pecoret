from rest_framework import serializers
from backend.api.serializers.user import MinimalUserSerializer
from backend.models import FindingComment


class FindingCommentSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer(read_only=True)
    user_edit = MinimalUserSerializer(read_only=True)

    class Meta:
        model = FindingComment
        fields = ["pk", "date_created", "date_updated", "user", "comment", "user_edit"]
