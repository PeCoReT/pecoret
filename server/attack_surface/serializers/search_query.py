from rest_framework import serializers

from attack_surface.models import UserSearchQuery


class UserSearchQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSearchQuery
        fields = ['query', 'name', 'pk', 'date_created', 'date_updated']
