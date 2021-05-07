from rest_framework import serializers

from blog.models import Blog, Tag
from media.serializer import MediaSerializer, MediaItemSerializer


class BlogListSerializer(serializers.ModelSerializer):
    author_full_name = serializers.CharField()
    image = MediaItemSerializer(required=False, read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'slug', 'title', 'image', 'content', 'author_full_name', 'published_on']


class BlogRetrieveSerializer(serializers.ModelSerializer):
    image = MediaSerializer(required=False, read_only=True)
    author_full_name = serializers.CharField()

    class Meta:
        model = Blog
        fields = '__all__'


class BlogCreateUpdateDestroySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)
    published_on = serializers.DateTimeField(required=False)
    created_date = serializers.DateTimeField(required=False)
    updated_date = serializers.DateTimeField(required=False)

    class Meta:
        model = Blog
        fields = '__all__'
