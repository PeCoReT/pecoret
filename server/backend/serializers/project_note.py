from rest_framework import serializers
from backend.models.project_note import ProjectNote


class ProjectNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectNote
        fields = [
            'pk', 'date_created', 'date_updated', 'title', 'text'
        ]
