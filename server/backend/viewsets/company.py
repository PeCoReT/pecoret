from backend.serializers.company import CompanySerializer, CustomerCompanySerializer
from backend.models import Company
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet


class CompanyViewSet(PeCoReTModelViewSet):
    queryset = Company.objects.none()
    search_fields = ["name"]
    api_scope = "scope_companies"
    serializer_class = CompanySerializer

    def get_permissions(self):
        if self.action in ["list"]:
            return [
                permissions.GroupPermission(
                    read_write_groups=[],
                    read_only_groups=[
                        permissions.Groups.GROUP_MANAGEMENT, permissions.Groups.GROUP_PENTESTER,
                        permissions.Groups.CUSTOMER
                    ]
                )
            ]
        if self.action == "create":
            return [
                permissions.GroupPermission(
                    read_write_groups=[
                        permissions.Groups.GROUP_MANAGEMENT
                    ],
                    read_only_groups=[]
                )
            ]
        return [
            permissions.CompanyPermission(
                read_write_groups=[
                    permissions.Groups.GROUP_PENTESTER,
                    permissions.Groups.GROUP_MANAGEMENT
                ],
                read_only_groups=[]
            )
        ]

    def get_serializer_class(self):
        if self.request.user.is_customer:
            return CustomerCompanySerializer
        return CompanySerializer

    def get_queryset(self):
        return Company.objects.for_user(self.request.user)
