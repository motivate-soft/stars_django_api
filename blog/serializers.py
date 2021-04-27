from rest_framework import serializers

from blog.models import Blog


class BlogListSerializer(serializers.ModelSerializer):
    """DRF Serializer Listing All The Blog Posts"""

    author_full_name = serializers.CharField()

    class Meta:
        model = Blog
        fields = ['slug', 'title', 'short_description', 'author_full_name', 'published_on']


class BlogDetailSerializer(serializers.ModelSerializer):
    """DRF Serializer For Details Of The Blog Posts"""

    author_full_name = serializers.CharField()

    class Meta:
        model = Blog
        fields = ['slug', 'title', 'body', 'author_full_name', 'published_on', 'short_description', 'created_date',
                  'updated_date']
