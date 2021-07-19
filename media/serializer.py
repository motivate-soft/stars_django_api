import os

from django.core.files.images import get_image_dimensions
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from rest_framework import serializers
from media.models import Media


# import environ
#
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#
# env = environ.Env()
# env.read_env(os.path.join(BASE_DIR, '.env'))


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = (
            'id', 'title', 'file', 'order', 'created_date', 'updated_date'
        )
        extra_kwargs = {'file': {'required': False, 'validators': []}}

    @receiver(pre_delete, sender=Media)
    def media_delete(sender, instance, **kwargs):
        # Pass false so FileField doesn't save the model.
        if instance.file:
            instance.file.delete(False)
    #
    # @receiver(models.signals.post_delete, sender=Media)
    # def auto_delete_file_on_delete(sender, instance, **kwargs):
    #     """
    #     Deletes file from filesystem
    #     when corresponding `Media` object is deleted.
    #     """
    #     if instance.file:
    #
    #         if os.path.isfile(instance.file.path):
    #             os.remove(instance.file.path)
    #
    # @receiver(models.signals.pre_save, sender=Media)
    # def auto_delete_file_on_change(sender, instance, **kwargs):
    #     """
    #     Deletes old file from filesystem
    #     when corresponding `Media` object is updated
    #     with new file.
    #     """
    #     if not instance.pk:
    #         return False
    #
    #     try:
    #         old_file = Media.objects.get(pk=instance.pk).file
    #     except Media.DoesNotExist:
    #         return False
    #
    #     new_file = instance.file
    #     if not old_file == new_file:
    #         if os.path.isfile(old_file.path):
    #             os.remove(old_file.path)

    # def get_file_url(self, obj):
    #     return obj.file.url


class MediaListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = (
            'id', 'title', 'file',
        )
        extra_kwargs = {'file': {'required': False, 'validators': []}}

    def to_representation(self, instance):
        representation = super(MediaListingSerializer, self).to_representation(instance)
        # representation['src'] = self.context['request'].build_absolute_uri('/' + instance.file.url)
        # representation['file'] = 'https://storage.googleapis.com/stars-website-react-2.appspot.com/' + instance.file.name
        return representation


"""
Return media file path
"""


class MediaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = (
            'id', 'title', 'file', 'order', 'created_date', 'updated_date'
        )
        extra_kwargs = {'file': {'required': False, 'validators': []}}

    def to_representation(self, instance):
        # is_production = env('PRODUCTION', cast=bool)
        # if not is_production:
        #     return self.context['request'].build_absolute_uri(instance.file.url)

        return self.context['request'].build_absolute_uri(instance.file.url)


"""
Return image width, height
"""


class MediaItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = (
            'id', 'title', 'file', 'order', 'created_date', 'updated_date'
        )

    def to_representation(self, instance):
        representation = super(MediaItemDetailSerializer, self).to_representation(instance)
        width, height = get_image_dimensions(instance.file.file)
        representation['width'] = width
        representation['height'] = height

        return representation


class PropertyMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = (
            'id', 'title', 'file', 'order'
        )
        extra_kwargs = {'file': {'required': False, 'validators': []}}

    def to_representation(self, instance):
        representation = super(PropertyMediaSerializer, self).to_representation(instance)
        # representation['src'] = self.context['request'].build_absolute_uri('/' + instance.file.url)
        # representation['file'] = 'https://storage.googleapis.com/stars-website-react-2.appspot.com/' + instance.file.name
        return representation
