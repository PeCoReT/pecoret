from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django_q.tasks import async_task
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.api.serializers import user as serializers
from backend.api.throttle import AuthFlowThrottle
from backend.models import User
from backend.tasks import mail
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTModelViewSet, PeCoReTReadOnlyModelViewSet


@extend_viewset_schema(tags=['Users'], verbose_name='user')
@extend_schema_view(
    update_profile=extend_schema(operation_id='Update user profile', tags=['Users']),
    change_email=extend_schema(operation_id='Initialize changing email', tags=['Users']),
    change_email_confirm=extend_schema(operation_id='Confirm changing email', tags=['Users']),
)
class UserViewSet(PeCoReTModelViewSet):
    queryset = User.objects.all()
    filterset_class = None
    search_fields = ["username", "first_name", "last_name"]
    api_scope = None
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[],
            read_only_groups=[permissions.Groups.GROUP_MANAGEMENT]
        )
    ]

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.UserCreateSerializer
        if self.action in ["update", "partial_update"]:
            return serializers.UserAdminUpdateSerializer
        return serializers.BaseUserSerializer

    @action(
        detail=False,
        methods=["patch"],
        serializer_class=serializers.UpdateProfileSerializer,
        permission_classes=[IsAuthenticated],
    )
    def update_profile(self, request, *args, **kwargs):
        obj = request.user
        serializer = serializers.UpdateProfileSerializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=False, methods=["post"], serializer_class=serializers.ChangeEmailSerializer,
            throttle_classes=[AuthFlowThrottle], permission_classes=[IsAuthenticated])
    @method_decorator(csrf_protect)
    def change_email(self, request, *args, **kwargs):
        serializer = serializers.ChangeEmailSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        if not User.objects.filter(email=serializer.validated_data["email"]).exists():
            # set new mail and send confirm mail
            self.request.user.new_email = serializer.validated_data["email"]
            self.request.user.save()
            context = {"user": self.request.user}
            # send to new email address
            async_task(mail.send_change_email_mail, context, self.request.user.new_email)
        return Response({"message": "check your inbox"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], serializer_class=serializers.ChangeEmailConfirmSerializer,
            permission_classes=[IsAuthenticated], throttle_classes=[AuthFlowThrottle])
    @method_decorator(csrf_protect)
    def change_email_confirm(self, request, *args, **kwargs):
        if not request.user.new_email:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.ChangeEmailConfirmSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        request.user.email = request.user.new_email
        request.user.new_email = None
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    list=extend_schema(
        tags=['Groups'], operation_id='Get all groups'
    ),
    retrieve=extend_schema(
        tags=['Groups'], operation_id='Get a specific group'
    )
)
class GroupViewSet(PeCoReTReadOnlyModelViewSet):
    queryset = Group.objects.all()
    filterset_class = None
    api_scope = None  # do not allow api token access
    search_fields = ["name"]
    permission_classes = [
        permissions.GroupPermission(read_write_groups=[], read_only_groups=[])
    ]
    serializer_class = serializers.GroupSerializer
