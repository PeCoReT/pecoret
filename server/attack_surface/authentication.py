from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import Scanner


class ScannerAuth(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('X-Scanner-Auth')
        if not auth_header:
            return None  # No token provided, let other authenticators handle this
        try:
            scanner = Scanner.objects.get(token=auth_header)
        except Scanner.DoesNotExist:
            raise AuthenticationFailed('Invalid scanner token')
        return AnonymousUser(), scanner
