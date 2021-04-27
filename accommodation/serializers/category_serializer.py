from accommodation.models.category import Category
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'slug', 'created_date', 'updated_date',
        )


class CategoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'slug', 'created_date', 'updated_date',
        )

    def to_representation(self, obj):
        return obj.name
