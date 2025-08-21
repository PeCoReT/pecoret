from backend.models.reports.report import Report
from .base import BasePermission


class ReportPermission(BasePermission):
    """permission class for a given report.
    the report is extracted from the url kwargs.
    if the report belongs to the project, access allowed.

    This permission **must** be used in combination with a ``ProjectPermission``
    """

    def has_permission(self, request, view):
        return self.has_object_permission(request, view, None)

    def has_object_permission(self, request, view, obj):
        qs = Report.objects.for_project(project=request.project).filter(
            pk=request.resolver_match.kwargs["report"]
        )
        if qs.exists():
            request.report = qs.get()
            return True
        return False
