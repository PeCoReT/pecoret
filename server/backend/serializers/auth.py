from rest_framework import serializers
from .user import UserMeSerializer


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class LoginResponseSerializer(serializers.Serializer):
    user = UserMeSerializer(read_only=True)
    csrf_token = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    """empty serializer. required to make spectacular happy
    """
