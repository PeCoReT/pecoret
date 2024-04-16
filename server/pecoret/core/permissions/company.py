from rest_framework.permissions import SAFE_METHODS
from backend.models import Company, APIToken
from .base import BasePermission
from .token.base import TokenPermissionMixin


class CompanyPermission(BasePermission, TokenPermissionMixin):
    def __init__(self, read_write_groups=[], read_only_groups=[]):
        super().__init__()
        self.read_only_groups = read_only_groups
        self.read_write_groups = read_write_groups

    def __call__(self):
        # required because `permission_class` requires a class and not an instance
        return self

    @staticmethod
    def company_from_request(request):
        """ extract the company from the request path
        """
        company_id = None
        try:
            if "company" in request.resolver_match.kwargs:
                company_id = int(request.resolver_match.kwargs["company"])
            if (
                    request.resolver_match.url_name.startswith("company-")
                    and "pk" in request.resolver_match.kwargs
            ):
                company_id = int(request.resolver_match.kwargs["pk"])
        except ValueError:
            return None
        try:
            project = Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            return None
        return project

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

    def _check_read_write(self, request):
        if request.user.groups.filter(name__in=self.read_write_groups):
            return True
        return False

    def _check_read_only(self, request):
        read_both = self.read_only_groups + self.read_write_groups
        if request.user.groups.filter(name__in=read_both):
            return True
        return False

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        company = self.company_from_request(request)
        if not company:
            return False
        company = Company.objects.for_user(user).filter(pk=company.pk)
        if not company.exists():
            return False
        company = company.get()
        if user.is_superuser:
            request.company = company
            return True
        if user.is_customer and user.company.pk == company.pk:
            # customers should not have api tokens at the moment, but check permissions to prevent future errors
            if isinstance(request.auth, APIToken):
                if not self.has_token_permission(request, view, None):
                    return False
            request.company = company
            return True
        if request.method not in SAFE_METHODS:
            allowed = self._check_read_write(request)
            if allowed:
                if isinstance(request.auth, APIToken):
                    if not self.has_token_permission(request, view, None):
                        return False
                    request.company = company
                    return True
                request.company = company
                return True
        else:
            allowed = self._check_read_only(request)
            if allowed:
                if isinstance(request.auth, APIToken):
                    if not self.has_token_permission(request, view, None):
                        return False
                request.company = company
                return True
        return False
