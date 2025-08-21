import base64

from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


def encode_uid(user_pk):
    """encode user id for usage in one-time links

    Args:
        user_pk (int): primary key of user

    Returns:
        str: encoded primary key of user
    """
    return force_str(urlsafe_base64_encode(force_bytes(user_pk)))


def decode_uid(user_pk):
    """decode user id which was used in one-time links

    Args:
        user_pk (int): primary key of user

    Returns:
        str: decoded user primary key
    """
    return force_str(urlsafe_base64_decode(user_pk))


def image64(data):
    encoded = base64.b64encode(data)
    return f"data:image/png;base64,{encoded.decode()}"
