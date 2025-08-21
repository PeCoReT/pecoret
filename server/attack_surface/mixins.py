import base64
import json
import time

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
            serializer.save()
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


class SearchQLMixin:
    """a mixin that offers django QL search with optional download of results"""
    search_ql_download = True

    def is_search_ql_download(self, request):
        return self.search_ql_download and request.GET.get('download')

    def get_download_response(self, qs):
        serializer = self.get_serializer(qs, many=True)
        response = Response(json.dumps(serializer.data), content_type='application/json')
        filename = f'search-results-{int(time.time())}.json'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    @action(detail=False, methods=['get'])
    def search(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        if request.GET.get('ql'):
            try:
                data = base64.b64decode(request.GET.get('ql').encode())
                qs = qs.djangoql(data.decode())
            except Exception as e:
                print(e)
                return Response({'search': 'Error processing search'}, status=status.HTTP_400_BAD_REQUEST)
        if self.is_search_ql_download(request):
            return self.get_download_response(qs)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
