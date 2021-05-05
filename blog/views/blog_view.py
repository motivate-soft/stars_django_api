from rest_framework import generics

from blog.models import Blog
from blog.serializers.blog_serializer import BlogListSerializer, BlogDetailSerializer, AdminBlogDetailSerializer, \
    AdminBlogListSerializer


class BlogListCreateAPIView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdminBlogDetailSerializer
        return AdminBlogListSerializer


class BlogRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogDetailSerializer
    lookup_field = 'slug'
