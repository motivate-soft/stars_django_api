from rest_framework import serializers
from company.models import Company
from media.models import Media
from media.serializer import MediaSerializer, MediaItemSerializer


class CompanySerializer(serializers.ModelSerializer):
    image = MediaSerializer(read_only=True, required=False)

    class Meta:
        model = Company
        fields = (
            'id', 'name', 'image', 'created_date', 'updated_date'
        )

    def create(self, validated_data):
        instance = Company.objects.create(**validated_data)
        request = self.context['request']
        image = request.data.get('image', None)
        if image is not None and image != "":
            instance.image = Media.objects.get(pk=image["id"])
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance = super(CompanySerializer, self).update(instance, validated_data)
        request = self.context['request']
        image = request.data.get('image', [])
        try:
            instance.image = Media.objects.get(pk=image["id"])
            instance.save()
        except:
            instance.save()

        return instance


class CompanyListingSerializer(serializers.ModelSerializer):
    image = MediaItemSerializer(read_only=True, required=False)

    class Meta:
        model = Company
        fields = (
            'id', 'name', 'image', 'created_date', 'updated_date'
        )
