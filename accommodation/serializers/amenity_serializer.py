from accommodation.models.amenity import Amenity
from rest_framework import serializers

from media.models import Media
from media.serializer import PropertyMediaSerializer


class AmenitySerializer(serializers.ModelSerializer):
    image = PropertyMediaSerializer(read_only=True, required=False)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.context['request'].method == 'GET':
    #         self.fields['image'] = MediaSerializer()
    #     else:
    #         self.fields['image'] = serializers.PrimaryKeyRelatedField(queryset=Media.objects.all())

    class Meta:
        model = Amenity
        fields = (
            'id', 'name', 'slug', 'image', 'created_date', 'updated_date'
        )

    def create(self, validated_data):
        instance = Amenity.objects.create(**validated_data)
        request = self.context['request']
        image = request.data.get('image', None)
        if image is not None and image != "":
            instance.image = Media.objects.get(pk=image["id"])
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance = super(AmenitySerializer, self).update(instance, validated_data)
        request = self.context['request']
        image = request.data.get('image', [])
        try:
            instance.image = Media.objects.get(pk=image["id"])
            instance.save()
        except:
            instance.save()

        return instance


class AmenityListingSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField('get_image_url')
    image = PropertyMediaSerializer(read_only=True, required=False)

    class Meta:
        model = Amenity
        fields = (
            'id', 'name', 'slug', 'image', 'created_date', 'updated_date'
        )

    # @staticmethod
    # def get_image_url(obj):
    #     return obj.image.file.url
