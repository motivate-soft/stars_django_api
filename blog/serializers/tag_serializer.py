from rest_framework import serializers

from blog.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'slug'
        )


class TagItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'slug'
        )

    def to_representation(self, obj):
        return obj.name
