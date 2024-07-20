from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.views import api_settings
from rest_framework.views import exception_handler


DRF_NON_FIELD_ERRORS = api_settings.NON_FIELD_ERRORS_KEY


def handle(exc, context):
    """
    translate django validation error which causes HTTP 500 status to DRF validation errors
    and HTTP 400
    source: https://djangotherightway.com/convert-django-validation-errors-to-drf-compatible-errors
    """
    if isinstance(exc, ValidationError):
        data = exc.message_dict
        exc = serializers.ValidationError(detail=data)
    return exception_handler(exc, context)
