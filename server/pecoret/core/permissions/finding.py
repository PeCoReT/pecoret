from backend.models.finding import Finding
from .base import BasePermission


class FindingPermission(BasePermission):
    """permission class for a given finding.
    the finding is extracted from the url kwargs.
    if the finding belongs to the project, access allowed.

    This permission **must** be used in combination with a ``ProjectPermission``
    """

    def has_permission(self, request, view):
        return self.has_object_permission(request, view, None)

    def has_object_permission(self, request, view, obj):
        finding = Finding.objects.for_project(project=request.project).filter(
            pk=request.resolver_match.kwargs["finding"]
        )
        if finding.exists():
            request.finding = finding.get()
            return True
        return False
