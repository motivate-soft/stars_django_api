from rest_framework import generics

from .serializers import BlogListSerializer, BlogDetailSerializer
from blog.models import Blog


class BlogListView(generics.ListCreateAPIView):
    """View For List All Published Blogs"""

    queryset = Blog.objects.filter(is_published=True)
    serializer_class = BlogListSerializer
    lookup_field = 'slug'


class BlogDetailView(generics.RetrieveDestroyAPIView):
    """View For The Details Of A Single Blog"""

    queryset = Blog.objects.all()
    serializer_class = BlogDetailSerializer
    lookup_field = 'slug'
