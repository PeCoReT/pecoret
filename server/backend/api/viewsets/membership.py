from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.status import HTTP_200_OK

from backend.models import Membership
from backend.models.membership import Roles
from backend.api.serializers.memberships import MembershipSerializer, MembershipCreateUpdateSerializer
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTModelViewSet


@extend_viewset_schema(tags=['Projects'], verbose_name='membership')
@extend_schema_view(
    me=extend_schema(operation_id='Get my membership', tags=['Projects'])
)
class MembershipViewSet(PeCoReTModelViewSet):
    queryset = Membership.objects.none()
    filterset_class = None
    search_fields = ['user__username']
    api_scope = None  # disable changing memberships through api tokens
    permission_classes = [permissions.PRESET_OWNER_OR_READ_ONLY]
    serializer_class = MembershipSerializer

    def get_queryset(self):
        return Membership.objects.for_project(self.request.project)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return MembershipSerializer
        return MembershipCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(project=self.request.project)

    def perform_destroy(self, instance):
        # check if user is only owner and prevent deletion
        if not Membership.objects.filter(project=instance.project, role=Roles.OWNER).exclude(pk=instance.pk).exists():
            raise ValidationError({"user": "Project requires at least one owner!"})
        return super().perform_destroy(instance)

    @action(detail=False, methods=["get"])
    def me(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return Response(status=HTTP_200_OK)
        try:
            obj = Membership.objects.get(user=request.user, project=request.project)
        except Membership.DoesNotExist:
            # should never happen because permissions were already checked
            raise Membership.DoesNotExist
        serializer = self.get_serializer(obj)
        return Response(serializer.data)
