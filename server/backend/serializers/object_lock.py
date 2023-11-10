from rest_framework import serializers
from backend.models.object_lock import ObjectLock
from .user import MinimalUserSerializer


class ObjectLockSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer()

    class Meta:
        model = ObjectLock
        fields = ['pk', 'last_seen', 'first_seen', 'user']
