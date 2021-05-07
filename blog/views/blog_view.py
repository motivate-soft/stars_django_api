from rest_framework import generics

from blog.models import Blog
from blog.serializers.blog_serializer import BlogCreateUpdateDestroySerializer, BlogRetrieveSerializer, \
    BlogListSerializer


class BlogListCreateAPIView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BlogCreateUpdateDestroySerializer
        return BlogListSerializer


class BlogRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogCreateUpdateDestroySerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BlogRetrieveSerializer
        return BlogCreateUpdateDestroySerializer
