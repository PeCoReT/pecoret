from rest_framework.permissions import SAFE_METHODS
from pecoret.core.permissions import GroupPermission
from asmonitor.models.program import Program
from backend.models import APIToken


class ASMonitorGroupPermission(GroupPermission):

    @staticmethod
    def program_from_request(request):
        """
        get a program from the request url path
        :param request:
        :return:
        """
        program_id = None
        try:
            if "program" in request.resolver_match.kwargs:
                program_id = request.resolver_match.kwargs['program']
            if request.resolver_match.url_name.startswith('program-') and 'pk' in request.resolver_match.kwargs:
                program_id = request.resolver_match.kwargs['pk']
        except ValueError:
            return None
        try:
            program = Program.objects.get(pk=program_id)
        except Program.DoesNotExist:
            return None
        return program

    def has_permission(self, request, view):
        """always check for object permission
        """
        return self.has_object_permission(request, view, None)

    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            allowed = self._check_read_write(request, view)
            if allowed:
                if isinstance(request.auth, APIToken):
                    if not self.has_token_permission(request, view, obj):
                        return False
        else:
            allowed = self._check_read_only(request, view)
            if allowed:
                if isinstance(request.auth, APIToken):
                    if not self.has_token_permission(request, view, obj):
                        return False
        if not allowed:
            return False
        request.program = self.program_from_request(request)
        return True
