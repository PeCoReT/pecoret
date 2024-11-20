from rest_framework import serializers
from backend.models.project_file import ProjectFile


class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = [
            "pk", "date_created", "date_updated", "name", "file"
        ]
