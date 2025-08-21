from django.http import FileResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models import Company
from backend.api.serializers.company import CompanySerializer, CustomerCompanySerializer
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core.utils.schema import extend_viewset_schema


@extend_viewset_schema(tags=["Companies"], verbose_name="companies")
class CompanyViewSet(PeCoReTModelViewSet):
    queryset = Company.objects.none()
    search_fields = ["name"]
    ordering_fields = ["date_created", "date_updated"]
    api_scope = "scope_companies"
    serializer_class = CompanySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [
                permissions.GroupPermission(
                    read_write_groups=[],
                    read_only_groups=[
                        permissions.Groups.GROUP_MANAGEMENT,
                        permissions.Groups.GROUP_PENTESTER,
                        permissions.Groups.CUSTOMER,
                    ],
                )
            ]
        if self.action == "create":
            return [
                permissions.GroupPermission(
                    read_write_groups=[permissions.Groups.GROUP_MANAGEMENT],
                    read_only_groups=[],
                )
            ]
        elif self.action == "destroy":
            return [
                permissions.GroupPermission(
                    read_write_groups=[permissions.Groups.GROUP_MANAGEMENT]
                )
            ]
        elif self.action in ["update", "partial_update"]:
            return [
                permissions.GroupPermission(
                    read_write_groups=[
                        permissions.Groups.GROUP_MANAGEMENT,
                        permissions.Groups.GROUP_PENTESTER,
                        permissions.Groups.CUSTOMER,
                    ]
                )
            ]
        return [
            permissions.GroupPermission(
                read_write_groups=[
                    permissions.Groups.GROUP_PENTESTER,
                    permissions.Groups.GROUP_MANAGEMENT,
                ],
                read_only_groups=[],
            )
        ]

    def get_serializer_class(self):
        # check auth here to make drf_spectacular not through error
        if self.request.user.is_authenticated and self.request.user.is_customer:
            return CustomerCompanySerializer
        return CompanySerializer

    def get_queryset(self):
        return Company.objects.for_user(self.request.user)

    @action(detail=True, methods=["get"])
    def logo(self, request, **kwargs):
        obj = self.get_object()
        if obj.logo:
            return FileResponse(obj.logo, content_type="image/png")
        return Response({}, status=status.HTTP_404_NOT_FOUND)
