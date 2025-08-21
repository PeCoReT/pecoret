from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


class LockedItemMixin:
    """
    handle item lock and unlock
    """
    @action(detail=True, methods=['post'])
    def lock(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.is_locked and obj.locked_by != request.user:
            raise ValidationError({'locked': 'item is already locked by another user'})
        obj.locked_by = request.user
        obj.locked_at = timezone.now()
        obj.save()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def unlock(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.is_locked and obj.locked_by != request.user:
            raise ValidationError({'locked': 'item is already locked by another user'})
        obj.locked_by = None
        obj.locked_at = None
        obj.save()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)
