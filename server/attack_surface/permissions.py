from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import SAFE_METHODS

from pecoret.core.permissions.group import GroupPermission
from attack_surface.models.scanner import Scanner


class ScanningPermission(GroupPermission):
    def __init__(self, read_write_groups=[], read_only_groups=[], scanner_write=False, scanner_read=False):
        super().__init__(read_write_groups=read_write_groups, read_only_groups=read_only_groups)
        self.scanner_write = scanner_write
        self.scanner_read = scanner_read

    def has_permission(self, request, view):
        if request.headers.get('X-Scanner-Auth'):
            return self._check_scanner_auth(request, view)
        return super().has_permission(request, view)

    def _check_scanner_auth(self, request, view):
        if request.method in SAFE_METHODS and self.scanner_read:
            return self.check_scanner_token(request)
        elif self.scanner_write:
            return self.check_scanner_token(request)
        raise PermissionDenied('Scanner not allowed')

    def check_scanner_token(self, request):
        auth_header = request.headers.get('X-Scanner-Auth')
        if not auth_header:
            raise PermissionDenied()
        try:
            scanner = Scanner.objects.get(token=auth_header)
        except Scanner.DoesNotExist:
            raise PermissionDenied('Invalid scanner token')
        request.scanner = scanner
        return True

