from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied, ValidationError

from .base import BasePermission


class LockedItemPermission(BasePermission):
    """
    checks if a user is locked by another user
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj and obj.is_locked and obj.locked_by != request.user:
            # we raise 400 here because it matches common REST API response codes better then 403
            raise ValidationError({'locked_by': 'Item is locked by another user'})
        return True
