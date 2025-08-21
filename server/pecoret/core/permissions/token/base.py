from django.utils import timezone
from rest_framework.permissions import SAFE_METHODS
from backend.models.api_token import APIToken, AccessChoices


class TokenPermissionMixin:

    def _set_last_used(self, token):
        token.date_last_used = timezone.now()
        token.save()

    def has_token_permission(self, request, view, obj):
        scope = getattr(view, "api_scope")
        if not scope:
            # API view does not have a `api_scope` attribute. Token access not allowed
            return False
        if isinstance(request.auth, APIToken):
            scope_attr = getattr(request.auth, scope)
            if not scope_attr:
                return False
            if scope_attr is AccessChoices.NO_ACCESS:
                return False
            if request.method in SAFE_METHODS:
                # in safe methods, we usually accept all access choices
                if scope_attr == AccessChoices.READ:
                    self._set_last_used(request.auth)
                    return True
                if scope_attr == AccessChoices.READ_WRITE:
                    self._set_last_used(request.auth)
                    return True
            if scope_attr == AccessChoices.READ_WRITE:
                self._set_last_used(request.auth)
                return True
        return False
