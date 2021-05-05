from rest_framework import generics

from blog.models import Blog
from blog.serializers.blog_serializer import BlogListSerializer, BlogDetailSerializer, AdminBlogDetailSerializer, \
    AdminBlogListSerializer

"""
Guest View
"""


class BlogListAPIView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer


class BlogRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogDetailSerializer


"""
Admin View
"""


class BlogListCreateAPIView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdminBlogDetailSerializer
        return AdminBlogListSerializer


class BlogRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = AdminBlogDetailSerializer
