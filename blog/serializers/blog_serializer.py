from rest_framework import serializers

from blog.models import Blog, Tag
from media.serializer import MediaSerializer, MediaItemSerializer

"""
Guest Blog serializers
"""


class BlogListSerializer(serializers.ModelSerializer):
    author_full_name = serializers.CharField()

    class Meta:
        model = Blog
        fields = ['slug', 'title', 'content', 'author_full_name', 'published_on']


class BlogDetailSerializer(serializers.ModelSerializer):
    author_full_name = serializers.CharField()

    class Meta:
        model = Blog
        fields = ['slug', 'title', 'content', 'tags', 'author_full_name', 'published_on', 'created_date',
                  'updated_date']


"""
Admin Blog serializers
"""


class AdminBlogListSerializer(serializers.ModelSerializer):
    author_full_name = serializers.CharField()
    image = MediaItemSerializer(required=False, read_only=True)

    class Meta:
        model = Blog
        fields = ['slug', 'title', 'image', 'content', 'author_full_name', 'published_on', 'created_date',
                  'updated_date']


class AdminBlogDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['slug', 'title', 'image', 'content', 'tags', 'author', 'published_on', 'created_date',
                  'updated_date']
