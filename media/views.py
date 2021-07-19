import base64

from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, \
    RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from accommodation.models import Property
from media.models import Media
from media.serializer import MediaSerializer

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    MEDIA LIST VIEW
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class MediaPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PaginatedMediaListView(ListAPIView):
    queryset = Media.objects.order_by('-created_date')
    # queryset = Media.objects.exclude(id__in=[]).order_by('-created_date')
    serializer_class = MediaSerializer
    pagination_class = MediaPagination


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                     MEDIA CRUD VIEW
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class MediaListCreateView(ListCreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

    def get_queryset(self):
        property_id = self.request.query_params.get('property_id', '')
        if property_id == '' or property_id == 'null' or property_id == 'undefined':
            queryset = Media.objects.order_by('-created_date')
        else:
            queryset = Media.objects.filter(property=property_id).order_by('order')
        return queryset

    def create(self, request, *args, **kwargs):
        request.data['title'] = request.FILES['file'].name
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        media_instance = serializer.save()
        property_id = request.data.get('property', None)

        if property_id:
            Property.objects.get(pk=property_id).gallery_imgs.add(media_instance)

        # Parse base64 string
        # img_format, img_b64_str = image_data.split(';base64,')
        # # ext = img_format.split('/')[-1]
        # imageObj = ContentFile(base64.b64decode(img_b64_str), request.data['title'])
        #
        # # Cropped image property id
        # media_instance = Media.objects.create(title=title, file=imageObj)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MediaRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
