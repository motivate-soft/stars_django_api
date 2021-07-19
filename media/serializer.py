import os

from django.core.files.images import get_image_dimensions
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from rest_framework import serializers
from media.models import Media


class MediaSerializer(serializers.ModelSerializer):
    """
    media detail
    """

    class Meta:
        model = Media
        fields = (
            'id', 'title', 'file', 'order', 'created_date', 'updated_date'
        )
        extra_kwargs = {'file': {'required': False, 'validators': []}}

    @receiver(pre_delete, sender=Media)
    def media_delete(sender, instance, **kwargs):
        if instance.file:
            instance.file.delete(False)

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


class MediaItemSerializer(serializers.ModelSerializer):
    """
    Return media file path
    """

    class Meta:
        model = Media
        fields = (
            '__all__'
        )
        extra_kwargs = {'file': {'required': False, 'validators': []}}

    def to_representation(self, instance):
        return self.context['request'].build_absolute_uri(instance.file.url)
