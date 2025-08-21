from pecoret.core.viewsets import PeCoReTModelViewSet
from backend.api.serializers.company_contact import CompanyContactSerializer
from backend.models.company_contact import CompanyContact
from backend.api.filters.company_contact import CompanyContactFilter
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema


@extend_viewset_schema(tags=['Companies'], verbose_name='company contact')
class CompanyContactViewSet(PeCoReTModelViewSet):
    permission_classes = [
        permissions.CompanyPermission(
            read_write_groups=[
                permissions.Groups.GROUP_MANAGEMENT,
                permissions.Groups.GROUP_PENTESTER,
                permissions.Groups.CUSTOMER
            ],
            read_only_groups=[]
        )
    ]
    api_scope = "scope_companies"
    queryset = CompanyContact.objects.none()
    search_fields = ["first_name", "last_name"]
    filterset_class = CompanyContactFilter
    serializer_class = CompanyContactSerializer

    def get_queryset(self):
        return CompanyContact.objects.for_company(self.request.company)

    def perform_create(self, serializer):
        serializer.save(company=self.request.company)
