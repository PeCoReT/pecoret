from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from rest_framework import serializers
from backend.models.user import User
from backend.api.serializers.company import CompanySerializer
from backend.utils.change_email_token_generator import change_email_token_generator
from pecoret.core.serializers import PrimaryKeyRelatedField
from pecoret.core.utils import decode_uid


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["name", "pk"]
        read_only = ["name"]


class BaseUserSerializer(serializers.ModelSerializer):
    company = PrimaryKeyRelatedField(serializer=CompanySerializer)

    class Meta:
        model = User
        fields = ["pk", "username", "first_name", "last_name", "is_active", "email", "groups", 'company']
        read_only_fields = ["pk", "username", "is_active", "groups"]


class UpdateProfileSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = ["pk", "first_name", "last_name", 'nickname']
        read_only_fields = ["pk"]


class MinimalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "pk"]
        read_only_fields = ["username", "pk"]


class UserCreateSerializer(serializers.ModelSerializer):
    default_error_messages = {
        "invalid_password": "Invalid password! {msg}"
    }

    class Meta:
        model = User
        fields = ["pk", "username", "first_name", "last_name", "email", "groups", 'company', 'password']
        read_only_Fields = ["pk", "username"]
        extra_kwargs = {
            'password': {'required': False, 'allow_null': True, 'allow_blank': True}
        }

    def create(self, validated_data):
        groups = validated_data.pop('groups')
        password = validated_data.pop('password', None)
        user = User.objects.create_user(**validated_data, is_active=False)
        if password:
            user.set_password(password)
        user.save()
        for group in groups:
            user.groups.add(group)
        return user

    def validate(self, attrs):
        if attrs.get('password'):
            user = self.context['request'].user
            try:
                validate_password(attrs["password"], user)
            except ValidationError as e:
                self.fail("invalid_password", msg=str(';'.join(list(e.messages))))
        group = Group.objects.get(name='Customer')
        if attrs.get('company') and group not in attrs['groups']:
            raise ValidationError({'company': 'Only customers can have a company set.'})
        if group in attrs['groups'] and not attrs.get('company'):
            raise ValidationError({'company': 'Customers must have an associated company set.'})
        return super().validate(attrs)


class UserAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "username", "first_name", "last_name", "email", "groups", "is_active", 'company']
        read_only_fields = ["username"]

    def validate(self, attrs):
        group = Group.objects.get(name='Customer')
        if attrs.get('company') and group not in attrs['groups']:
            raise ValidationError({'company': 'Only customers can have a company set.'})
        if group in attrs['groups'] and not attrs.get('company'):
            raise ValidationError({'company': 'Customers must have an associated company set.'})
        return super().validate(attrs)


class UserMeSerializer(serializers.ModelSerializer):
    # output all details of the logged-in user
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["pk", "username", "first_name", "last_name", "is_active", "email", "groups", "is_superuser", "nickname"]
        read_only_Fields = ["pk", "username", "is_active", "groups", "is_superuser"]


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def get_user(self):
        try:
            user = User.objects.get(is_active=True, email=self.data.get("email"))
            if user.has_usable_password():
                return user
        except User.DoesNotExist:
            pass


class PasswordResetConfirmSerializer(serializers.Serializer):
    default_error_messages = {
        "invalid_password": "Invalid password! {msg}",
        "invalid_token": "Token is not valid",
        "invalid_uid": "Invalid user!"
    }
    new_password = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        try:
            uid = decode_uid(self.initial_data.get("uid", ""))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            self.fail("invalid_uid")
        is_token_valid = default_token_generator.check_token(user, self.initial_data.get("token", ""))
        if not is_token_valid:
            self.fail("invalid_token")
        try:
            validate_password(attrs["new_password"], user)
        except ValidationError as e:
            self.fail("invalid_password", msg=str(';'.join(list(e.messages))))
        self.user = user
        return validated_data


class ChangeEmailConfirmSerializer(serializers.Serializer):
    default_error_messages = {
        "invalid_token": 'Token is not valid',
        'invalid_uid': 'Invalid user!'
    }

    def validate(self, attrs):
        validated_Data = super().validate(attrs)
        try:
            uid = decode_uid(self.initial_data.get('uid', ''))
            user = User.objects.get(pk=uid)
            # ensure, that no one has stolen my token, since my password was already supplied.
            # user2 should not be able to submit tokens of user1
            if self.context['request'].user.pk is not user.pk:
                self.fail("invalid_uid")
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            self.fail("invalid_uid")
        is_token_valid = change_email_token_generator.check_token(user, self.initial_data.get('token'))
        if not is_token_valid:
            self.fail("invalid_token")
        self.user = user
        return validated_Data


class ChangeEmailSerializer(serializers.Serializer):
    default_error_messages = {"invalid_password": "password incorrect!"}

    password = serializers.CharField()
    email = serializers.EmailField()

    def validate_password(self, value):
        request = self.context["request"]
        if request.user.check_password(value):
            return True
        self.fail("invalid_password")
