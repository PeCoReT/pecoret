from rest_framework.permissions import SAFE_METHODS
from backend.models.api_token import APIToken
from .base import BasePermission
from .token.base import TokenPermissionMixin


class Groups(object):
    GROUP_PENTESTER = 'Pentester'
    GROUP_MANAGEMENT = 'Management'
    CUSTOMER = 'Customer'


class GroupPermission(BasePermission, TokenPermissionMixin):
    def __init__(self, read_write_groups=[], read_only_groups=[]):
        super().__init__()
        self.read_write_groups = read_write_groups
        self.read_only_groups = read_only_groups

    def __call__(self):
        # required because `permission_class` requires a class and not an instance
        return self

    @staticmethod
    def check_superuser(groups):
        return True

    def _check_read_write(self, request, view):
        if request.user.is_superuser:
            return self.check_superuser(self.read_write_groups)
        if request.user.groups.filter(name__in=self.read_write_groups):
            if isinstance(request.auth, APIToken):
                if not self.has_token_permission(request, view, None):
                    return False
            return True
        return False

    def _check_read_only(self, request, view):
        read_both = self.read_only_groups + self.read_write_groups
        if request.user.is_superuser:
            return self.check_superuser(read_both)
        if request.user.groups.filter(name__in=read_both):
            if isinstance(request.auth, APIToken):
                if not self.has_token_permission(request, view, None):
                    return False
            return True
        return False

    def has_permission(self, request, view):
        if request.method not in SAFE_METHODS:
            return self._check_read_write(request, view)
        return self._check_read_only(request, view)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
