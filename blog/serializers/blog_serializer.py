from rest_framework import serializers

from blog.models import Blog
from blog.serializers.tag_serializer import TagItemSerializer
from media.serializer import MediaSerializer, MediaItemSerializer

"""
Guest
"""


class BlogDetailSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)
    published_date = serializers.DateTimeField(required=False)
    author_full_name = serializers.CharField()
    image = MediaItemSerializer(required=False, read_only=True)
    tags = TagItemSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'


class BlogListingSerializer(serializers.ModelSerializer):
    author_full_name = serializers.CharField()
    image = MediaItemSerializer(required=False, read_only=True)
    tags = TagItemSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'slug', 'title', 'image', 'tags', 'content', 'author_full_name', 'published_date']


"""
Admin
"""


class BlogListSerializer(serializers.ModelSerializer):
    author_full_name = serializers.CharField()
    image = MediaItemSerializer(required=False, read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'slug', 'title', 'image', 'tags', 'content', 'author_full_name', 'published_date']


class BlogRetrieveSerializer(serializers.ModelSerializer):
    image = MediaSerializer(required=False, read_only=True)
    author_full_name = serializers.CharField()

    class Meta:
        model = Blog
        fields = '__all__'


class BlogCreateUpdateDestroySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)
    published_date = serializers.DateTimeField(required=False)
    created_date = serializers.DateTimeField(required=False)
    updated_date = serializers.DateTimeField(required=False)

    class Meta:
        model = Blog
        fields = '__all__'
