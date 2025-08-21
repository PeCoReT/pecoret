from rest_framework import serializers
from django_q.models import Task


class DjangoQTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["stopped", "started", "success"]
