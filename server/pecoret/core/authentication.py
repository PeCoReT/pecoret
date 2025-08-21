from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from backend.models import APIToken


class APITokenAuthentication(TokenAuthentication):
    """this is a custom token authentication.

    Raises:
        exceptions.AuthenticationFailed: If token is invalid or expired.

    Returns:
        tuple: current user, used token
    """
    model = APIToken
    keyword = "Bearer"

    def authenticate_credentials(self, key):
        prefix, token = key.split(".")
        qs = self.model.objects.filter(prefix=prefix)
        if not qs.exists():
            raise exceptions.AuthenticationFailed("No such token found!")
        api_token = qs.get()
        if api_token.is_expired():
            api_token.delete()
            raise exceptions.AuthenticationFailed("Token expired")
        if api_token.is_valid(token):
            return api_token.user, api_token
        raise exceptions.AuthenticationFailed("No such token found!")
