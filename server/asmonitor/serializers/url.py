from rest_framework import serializers
from django_q.tasks import async_task
from asmonitor import tasks
from asmonitor import utils
from asmonitor.models import URL
from asmonitor.models.port import Port, Protocol
from asmonitor.serializers.tag import TagSerializer
from backend.serializers.technology import TechnologySerializer
from pecoret.core.serializers import PrimaryKeyRelatedField
from .program import ProgramSerializer
from .target import TargetSerializer


class URLSerializer(serializers.ModelSerializer):
    technologies = PrimaryKeyRelatedField(serializer=TechnologySerializer, many=True, required=False)
    tags = PrimaryKeyRelatedField(serializer=TagSerializer, many=True, required=False)

    class Meta:
        model = URL
        fields = [
            'pk', 'url', 'date_created', 'date_updated', 'last_seen', 'request', 'response', 'status_code',
            'is_base', 'technologies', 'tags'
        ]

    def create(self, validated_data):
        instance = super().create(validated_data)
        scheme, port = utils.url.port_and_scheme_from_url(instance.url)
        _, _ = Port.objects.get_or_create(target=instance.target, port=port, protocol=Protocol.TCP,
                                          defaults={'service': scheme})
        async_task(tasks.sync_implicit_techs_url, instance.pk)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        async_task(tasks.sync_implicit_techs_url, instance.pk)
        return instance


class GlobalURLSerializer(URLSerializer):
    program = PrimaryKeyRelatedField(serializer=ProgramSerializer)
    target = PrimaryKeyRelatedField(serializer=TargetSerializer)

    class Meta:
        model = URL
        fields = ['pk', 'url', 'date_created', 'date_updated', 'last_seen', 'program', 'status_code', 'target',
                  'is_base', 'technologies', 'tags']
