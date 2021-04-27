import base64

from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from accommodation.models import Property
from media.models import Media
from media.serializer import MediaSerializer

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    MEDIA LIST VIEW
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class PropertyMediaListView(ListAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

    def get_queryset(self):
        property_id = self.request.query_params.get('property_id', '')
        if property_id == '' or property_id == 'null' or property_id == 'undefined':
            queryset = Media.objects.order_by('-created_date')
        else:
            queryset = Media.objects.filter(property=property_id).order_by('order')
        return queryset


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
                    MEDIA BULK UPDATE VIEW
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class MediaMultipleUpdate(APIView):
    @staticmethod
    def get_object(obj_id):
        try:
            return Media.objects.get(id=obj_id)
        except (Media.DoesNotExist, ValidationError):
            raise status.HTTP_400_BAD_REQUEST

    @staticmethod
    def validate_ids(id_list):
        for id in id_list:
            try:
                Media.objects.get(id=id)
            except (Media.DoesNotExist, ValidationError):
                raise status.HTTP_400_BAD_REQUEST
        return True

    def put(self, request, *args, **kwargs):
        items = request.data
        id_list = [data['id'] for data in items]
        self.validate_ids(id_list=id_list)
        instances = []
        for key, value in enumerate(d['id'] for d in items):
            obj = self.get_object(obj_id=value)
            obj.order = key + 1
            obj.save()
            instances.append(obj)
        serializer = MediaSerializer(instances, many=True)
        return Response(serializer.data)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                     MEDIA CRUD VIEW
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class MediaCreateView(CreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

    def post(self, request, *args, **kwargs):
        if len(request.FILES) != 0:
            request.data['title'] = request.FILES['file'].name
            return self.create(request, *args, **kwargs)
        else:
            property_id = request.data.get('property', None)
            title = request.data.get('title', None)
            image_data = request.data.get('imageData', None)

            # Parse base64 string
            img_format, img_b64_str = image_data.split(';base64,')
            # ext = img_format.split('/')[-1]
            imageObj = ContentFile(base64.b64decode(img_b64_str), request.data['title'])

            # Cropped image property id
            media_instance = Media.objects.create(title=title, file=imageObj)
            # property_instance = Property.objects.get(pk=property_id).gallery_imgs.add(media_instance)

            serializer = MediaSerializer(media_instance)
            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MediaRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
