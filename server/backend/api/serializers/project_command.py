from rest_framework import serializers
from backend.models.project_command import ProjectCommand
from .user import MinimalUserSerializer


class ProjectCommandSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer(read_only=True)

    class Meta:
        model = ProjectCommand
        fields = ["pk", "command", "output", "date_run", "user"]
