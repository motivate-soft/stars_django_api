from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accommodation.models import Amenity
from accommodation.serializers.amenity_serializer import AmenitySerializer, AmenityListingSerializer


class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer

    def get_serializer_class(self):
        if self.action == 'listing':
            return AmenityListingSerializer
        return AmenitySerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'listing':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False)
    def listing(self, request):
        queryset = Amenity.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
