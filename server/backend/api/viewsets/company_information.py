from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions
from backend.models.company_information import CompanyInformation
from backend.api.serializers.company_information import CompanyInformationSerializer
from backend.api.filters.company_information import CompanyInformationFilter
from pecoret.core.utils.schema import extend_viewset_schema


@extend_viewset_schema(verbose_name='company information', tags=['Companies'])
class CompanyInformationViewSet(PeCoReTModelViewSet):
    queryset = CompanyInformation.objects.none()
    filterset_class = CompanyInformationFilter
    serializer_class = CompanyInformationSerializer
    api_scope = "scope_companies"
    permission_classes = [
        permissions.CompanyPermission(
            read_write_groups=[
                permissions.Groups.GROUP_PENTESTER,
                permissions.Groups.GROUP_MANAGEMENT,
                permissions.Groups.CUSTOMER
            ],
            read_only_groups=[]
        )
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, company=self.request.company)

    def get_queryset(self):
        return CompanyInformation.objects.for_company(self.request.company)

    def perform_update(self, serializer):
        serializer.save(user_edit=self.request.user, company=self.request.company)
