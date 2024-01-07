from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django_q.tasks import async_task
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from backend.models import User
from backend.serializers import user as serializers
from backend.tasks import mail
from backend.throttle import AuthFlowThrottle
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet, PeCoReTReadOnlyModelViewSet


class UserViewSet(PeCoReTModelViewSet):
    queryset = User.objects.all()
    filterset_class = None
    search_fields = ["username", "first_name", "last_name"]
    api_scope = None
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[], read_only_groups=[permissions.Groups.GROUP_MANAGEMENT]
        )
    ]

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.UserCreateSerializer
        if self.action in ["update", "partial_update"]:
            return serializers.UserAdminUpdateSerializer
        return serializers.BaseUserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        context = {"user": instance}
        async_task(mail.send_activation_mail, context, instance.email)

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

    @action(
        detail=False,
        methods=["post"],
        serializer_class=serializers.PasswordResetSerializer,
        permission_classes=[AllowAny],
        throttle_classes=[AuthFlowThrottle],
    )
    def reset_password(self, request, *args, **kwargs):
        logout(request)
        serializer = serializers.PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()
        if user:
            context = {"user": user}
            async_task(mail.send_password_reset_mail, context, user.email)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["post"],
        serializer_class=serializers.PasswordResetConfirmSerializer,
        permission_classes=[AllowAny],
    )
    def reset_password_confirm(self, request, *args, **kwargs):
        serializer = serializers.PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.user.set_password(serializer.data["new_password"])
        serializer.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["post"],
        serializer_class=serializers.ActivationSerializer,
        permission_classes=[AllowAny],
    )
    @method_decorator(csrf_protect)
    def activation(self, request, *args, **kwargs):
        serializer = serializers.ActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        serializer.user.set_password(serializer.data["new_password"])
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"], serializer_class=serializers.ChangeEmailSerializer,
            throttle_classes=[AuthFlowThrottle], permission_classes=[IsAuthenticated],

            )
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

    @action(detail=False, methods=['post'], serializer_class=serializers.PasswordChangeSerializer,
            permission_classes=[IsAuthenticated], throttle_classes=[AuthFlowThrottle])
    @method_decorator(csrf_protect)
    def change_password(self, request, *args, **kwargs):
        serializer = serializers.PasswordChangeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        update_session_auth_hash(request, request.user)
        return Response({'message': 'Password changed!'}, status=status.HTTP_200_OK)


class GroupViewSet(PeCoReTReadOnlyModelViewSet):
    queryset = Group.objects.all()
    filterset_class = None
    search_fields = ["name"]
    permission_classes = [
        permissions.GroupPermission(read_write_groups=[], read_only_groups=[])
    ]
    serializer_class = serializers.GroupSerializer
