from django_q.tasks import async_task
from drf_spectacular.utils import extend_schema_view, extend_schema

from backend.tasks import mail
from advisories.models.advisory_membership import AdvisoryMembership, Roles
from advisories.serializers.membership import (
    AdvisoryMembershipSerializer,
    AdvisoryMembershipCreateSerializer,
)
from pecoret.core.viewsets import PeCoReTNoUpdateViewSet
from pecoret.core import permissions


@extend_schema_view(
    list=extend_schema(operation_id='Get all advisory memberships', tags=['Advisories']),
    retrieve=extend_schema(operation_id='Get a specific advisory membership', tags=['Advisories']),
    destroy=extend_schema(operation_id='Delete a advisory membership', tags=['Advisories']),
    create=extend_schema(operation_id='Create a new advisory membership', tags=['Advisories'])
)
class AdvisoryMembershipViewSet(PeCoReTNoUpdateViewSet):
    queryset = AdvisoryMembership.objects.none()
    api_scope = "scope_advisories"
    permission_classes = [
        permissions.AdvisoryPermission(
            read_only_roles=[Roles.CREATOR, Roles.READ_ONLY, Roles.VENDOR]
        )
    ]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AdvisoryMembershipSerializer
        return AdvisoryMembershipCreateSerializer

    def get_queryset(self):
        return AdvisoryMembership.objects.for_advisory(self.request.advisory)

    def perform_create(self, serializer):
        instance = serializer.save(advisory=self.request.advisory)
        context = {
            "advisoryId": self.request.advisory.pk,
            "vendor_name": self.request.advisory.technology.vendor,
        }
        async_task(mail.send_advisory_shared_mail, context, instance.user.email)
