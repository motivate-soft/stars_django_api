from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from blog.models import Blog
from blog.serializers.blog_serializer import BlogCreateUpdateDestroySerializer, BlogRetrieveSerializer, \
    BlogListSerializer, BlogListingSerializer, BlogDetailSerializer

"""
Guest 
"""


class BlogPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class BlogListingAPIView(generics.ListAPIView):
    queryset = Blog.objects.order_by('-created_date')
    # queryset = Blog.objects.all()
    serializer_class = BlogListingSerializer
    permission_classes = []
    pagination_class = BlogPagination

    def get_queryset(self):
        tags = self.request.query_params.get('tags', None)
        if tags:
            array = []
            for tag_id in tags.split(","):
                array.append(int(tag_id))
                print("___", array)
            queryset = Blog.objects.filter(tags__in=array).order_by('-published_date')
        else:
            queryset = Blog.objects.order_by('-published_date')
        return queryset


class BlogDetailAPIView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    permission_classes = []
    serializer_class = BlogDetailSerializer
    lookup_field = 'slug'


"""
Admin 
"""


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
