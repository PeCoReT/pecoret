from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.encoding import smart_str
from rest_framework import serializers
from generic_relations.relations import GenericRelatedField
from attack_surface.models import ScanObject, Host, Target, Service, URL, Port
from attack_surface.serializers.host import HostSerializer
from attack_surface.serializers.port import PortSerializer
from attack_surface.serializers.service import ServiceSerializer
from attack_surface.serializers.target import TargetSerializer
from attack_surface.serializers.url import URLSerializer


class ContentTypeRelatedField(serializers.SlugRelatedField):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(app_label='attack_surface')

    def to_internal_value(self, data):
        if isinstance(data, ContentType):
            return data
        queryset = self.get_queryset()
        try:
            return queryset.get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_str(data))
        except (TypeError, ValueError):
            self.fail('invalid')


class ScanObjectSerializer(serializers.ModelSerializer):
    content_type = ContentTypeRelatedField(slug_field='model', queryset=ContentType.objects.all())
    object_id = serializers.IntegerField()
    asset = GenericRelatedField(read_only=True, serializers={
        Host: HostSerializer(),
        Target: TargetSerializer(),
        Service: ServiceSerializer(),
        URL: URLSerializer(),
        Port: PortSerializer()
    })

    class Meta:
        model = ScanObject
        fields = [
            'content_type', 'object_id', 'asset'
        ]

    def validate(self, attrs):
        try:
            _object = attrs['content_type'].get_object_for_this_type(pk=attrs['object_id'])
        except ObjectDoesNotExist:
            raise ValidationError({'scan_object': 'No scan object with this ID'})
        return super().validate(attrs)
