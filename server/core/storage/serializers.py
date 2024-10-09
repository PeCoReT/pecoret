from rest_framework import serializers
from .models import ImageFile


class ImageFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageFile
        fields = [
            "pk", "date_created", "date_updated",
            "image", 'storage_link', 'name'
        ]
        extra_kwargs = {
            'image': {'write_only': True},
            'name': {'read_only': True},
        }

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.upload_directory = self.context['image_file_upload_directory']
        instance.save()
        return instance
