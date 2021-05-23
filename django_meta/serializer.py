from rest_framework import serializers
from rest_framework.fields import JSONField

from django_meta.models import ModelMeta


class MetaSerializer(serializers.ModelSerializer):
    # meta_tags = JSONField(required=False)
    # og_tags = JSONField(required=False)
    # twitter_tags = JSONField(required=False)

    class Meta:
        model = ModelMeta
        fields = (
            '__all__'
        )
