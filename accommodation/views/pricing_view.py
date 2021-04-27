from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accommodation.models import Price
from accommodation.serializers.price_serializer import PriceItemSerializer


class PriceItemViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceItemSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'filtered_list':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False)
    def filtered_list(self, request):
        property_id = self.request.query_params.get('property_id', None)
        queryset = Price.objects.filter(property=property_id).order_by('start_date')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
