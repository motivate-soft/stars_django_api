import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from blog.models import Blog
from blog.serializers.blog_serializer import BlogCreateUpdateDestroySerializer, BlogRetrieveSerializer, \
    BlogListSerializer, BlogListingSerializer, BlogDetailSerializer

"""
Guest 
"""


class M2MFilter(django_filters.Filter):

    def filter(self, qs, value):
        if not value:
            return qs

        values = value.split(',')

        """
        Chain queryset | AND
        """
        # for v in values:
        #     qs = qs.filter(labels=v)
        # return qs

        """
        Union queryset | OR
        """
        qs_array = []
        for v in values:
            qs_array.append(qs.filter(tags=v))

        index = 1
        result_qs = qs_array[0]

        while index < len(qs_array):
            result_qs = result_qs.union(qs_array[index])
            index = index + 1

        return result_qs


class BlogFilter(django_filters.FilterSet):
    tags = M2MFilter(field_name='tags')

    # tags = django_filters.filters.BaseInFilter(
    #     field_name='tags',
    #     lookup_expr='in',
    # )

    class Meta:
        model = Blog
        fields = ('tags',)


class BlogPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class BlogListingAPIView(generics.ListAPIView):
    ordering = '-published_date'
    ordering_fields = '-published_date'
    queryset = Blog.objects.order_by('-published_date')
    serializer_class = BlogListingSerializer
    permission_classes = []
    pagination_class = BlogPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = BlogFilter

    # def get_queryset(self):
    #     queryset = Blog.objects.order_by('-created_date')
    #     tags = self.request.query_params.get('tags', None)
    #     if tags:
    #         array = tags.split(",")
    #         queryset = Blog.objects.filter(tags__in=array).order_by('-created_date')
    #     else:
    #         queryset = Blog.objects.order_by('-created_date')
    #     return queryset


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
