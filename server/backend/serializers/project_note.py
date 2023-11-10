from rest_framework import serializers
from django.core.exceptions import ValidationError
from backend.models.project_note import ProjectNote
from .object_lock import ObjectLockSerializer


class ProjectNoteSerializer(serializers.ModelSerializer):
    object_lock = ObjectLockSerializer(source='object_lock_instance', read_only=True)

    class Meta:
        model = ProjectNote
        fields = [
            'pk', 'date_created', 'date_updated', 'title', 'text', 'object_lock'
        ]

    def save(self, **kwargs):
        if not self.instance or not self.instance.object_lock_instance:
            kwargs.pop('current_user')
            return super().save(**kwargs)
        current_user = self.context['request'].user
        if current_user.pk == self.instance.object_lock_instance.user.pk:
            return super().save(**kwargs)
        raise ValidationError({'self': 'object is locked'})
