from rest_framework.permissions import SAFE_METHODS
from backend.models import Advisory, AdvisoryMembership, APIToken
from backend.models.advisory import VisibilityChoices
from .base import BasePermission
from .token.base import TokenPermissionMixin


class AdvisoryPermission(BasePermission, TokenPermissionMixin):
    def __init__(self, read_write_roles=[], read_only_roles=[]):
        super().__init__()
        self.read_only_roles = read_only_roles
        self.read_write_roles = read_write_roles

    def __call__(self):
        # required because `permission_class` requires a class and not an instance
        return self

    @staticmethod
    def advisory_from_request(request):
        """get advisory from request url path

        Args:
            request (_type_): _description_

        Returns:
            Advisory: The advisory that was extracted. Return none if no advisory was found
        """
        advisory_id = None
        try:
            if "advisory" in request.resolver_match.kwargs:
                advisory_id = request.resolver_match.kwargs["advisory"]
            if (
                    request.resolver_match.url_name.startswith("advisory-")
                    and "pk" in request.resolver_match.kwargs
            ):
                advisory_id = request.resolver_match.kwargs["pk"]
        except ValueError:
            return None
        try:
            advisory = Advisory.objects.get(pk=advisory_id)
        except Advisory.DoesNotExist:
            return None
        return advisory

    def has_permission(self, request, view):
        """always check for object permission
        """
        return self.has_object_permission(request, view, None)

    def has_object_permission(self, request, view, obj):
        advisory = self.advisory_from_request(request)
        # block unauthenticated access
        if not advisory or not request.user.is_authenticated:
            return False
        # shared with advisory management team
        if advisory.visibility == VisibilityChoices.TEAM:
            if request.user.groups.filter(name='Advisory Management').exists():
                if isinstance(request.auth, APIToken):
                    if not self.has_token_permission(request, view, obj):
                        return False
                request.advisory = advisory
                return True

        # check memberships
        membership = AdvisoryMembership.objects.filter(user=request.user, advisory=advisory)
        if not membership.exists():
            # no membership found - deny access
            return False
        if not membership.get().active:
            # membership exists, but is expired - deny access
            membership.delete()
            return False
        if request.method in SAFE_METHODS:
            both_values = self.read_only_roles + self.read_write_roles
            allowed = membership.filter(role__in=both_values).exists()
            if allowed:
                if isinstance(request.auth, APIToken):
                    if not self.has_token_permission(request, view, obj):
                        return False
                request.advisory = advisory
            return allowed
        allowed = membership.filter(role__in=self.read_write_roles).exists()
        if allowed:
            if isinstance(request.auth, APIToken):
                if not self.has_token_permission(request, view, obj):
                    return False
            request.advisory = advisory
        return allowed
