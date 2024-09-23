from django.conf import settings
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from attack_surface.authentication import ScannerAuth
from pecoret.core.authentication import APITokenAuthentication


class CreateOrUpdateMixin:
    def get_create_or_update_queryset(self, request):
        raise NotImplementedError()

    @action(detail=False, methods=['post'])
    def create_or_update(self, request, *args, **kwargs):
        qs = self.get_create_or_update_queryset(request)
        if qs.exists():
            serializer = self.get_serializer(qs.get(), data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status.HTTP_200_OK)
        # create
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ScanFeatureDispatchMixin:
    """checks if feature is enabled """

    def dispatch(self, request, *args, **kwargs):
        if not settings.AS_ENABLE_SCANNING:
            self.headers = self.default_response_headers
            response = Response({'detail': 'Feature is disabled'}, status=status.HTTP_400_BAD_REQUEST)
            return self.finalize_response(request, response, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


class ScanningAuthMixin:
    authentication_classes = [ScannerAuth, SessionAuthentication, APITokenAuthentication]
