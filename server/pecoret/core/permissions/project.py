from django.db.models import Q
from rest_framework.permissions import SAFE_METHODS

from backend.models import APIToken
from backend.models.membership import Membership
from backend.models.project import Project, Visibility
from pecoret.core.permissions.group import Groups
from .base import BasePermission
from .token.base import TokenPermissionMixin


class ProjectPermission(BasePermission, TokenPermissionMixin):
    def __init__(self, read_write_roles=[], read_only_roles=[]):
        super().__init__()
        self.read_only_roles = read_only_roles
        self.read_write_roles = read_write_roles

    def _check_project_membership(self, user, project):
        return Membership.objects.for_project(project).for_user(user)

    @staticmethod
    def project_from_request(request):
        """extract the project from the request path

        Args:
            request (_type_): _description_

        Returns:
            Project: the project that was specified in the request path
        """
        project_id = None
        try:
            if "project" in request.resolver_match.kwargs:
                project_id = int(request.resolver_match.kwargs["project"])
            if (
                    request.resolver_match.url_name.startswith("project-")
                    and "pk" in request.resolver_match.kwargs
            ):
                project_id = int(request.resolver_match.kwargs["pk"])
        except ValueError:
            return None
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return None
        return project

    def has_object_permission(self, request, view, obj):
        project = self.project_from_request(request)
        if not project or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            request.project = project
            return True
        # allow public projects for pentesters and management users
        if project.visibility == Visibility.PENTESTERS:
            if request.user.is_pentester_or_management:
                request.project = project
                return True

        membership = self._check_project_membership(request.user, project)
        if not membership.exists():
            return False
        if not membership.get().active:
            membership.delete()
            return False
        if request.method in SAFE_METHODS:
            # allow read_write roles to read
            both_values = self.read_write_roles + self.read_only_roles
            allowed = membership.for_roles(both_values).exists()
            if allowed:
                if isinstance(request.auth, APIToken):
                    if self.has_token_permission(request, view, obj):
                        request.project = project
                        return True
                    else:
                        return False
                request.project = project
            return allowed
        # if method is not safe, then only members for specified roles are allowed to continue
        allowed = membership.for_roles(self.read_write_roles).exists()
        if allowed:
            if isinstance(request.auth, APIToken):
                if self.has_token_permission(request, view, obj):
                    request.project = project
                    return True
                return False
            request.project = project
        return allowed
