from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accommodation.models import Price, Property
from accommodation.models.price import MonthlyPrice
from accommodation.serializers.price_serializer import PriceItemSerializer, MonthlyPriceItemSerializer, \
    MonthlyPriceSerializer


class PriceItemViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceItemSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        property = self.request.query_params.get('property', None)
        queryset = Price.objects.all()
        if property:
            queryset = queryset.filter(property=property)
        return queryset.order_by('start_date')


class MonthlyPriceViewSet(viewsets.ModelViewSet):
    queryset = MonthlyPrice.objects.all()
    serializer_class = MonthlyPriceItemSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'bulk_create':
            return MonthlyPriceSerializer
        else:
            return MonthlyPriceItemSerializer

    def get_queryset(self):
        property = self.request.query_params.get('property', None)
        queryset = MonthlyPrice.objects.all()
        if property:
            queryset = queryset.filter(property=property)
        return queryset.order_by('date')

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        property_id = serializer.data['items'][0]['property']
        # old_items = MonthlyPrice.objects.filter(property=property_id).values_list('id', flat=True)
        items = MonthlyPrice.objects.filter(property=property_id)
        old_items = [item.id for item in items]
        updated_items = []
        for item in serializer.data['items']:
            property_instance = Property.objects.get(pk=item['property'])
            item['property'] = property_instance

            obj, created = MonthlyPrice.objects.update_or_create(
                date=item['date'], property=item['property'],
                defaults={'price': item['price']},
            )
            obj.save()
            if not created:
                updated_items.append(obj.id)

            # item_id = item.pop("id", None)
            # if item_id:
            #     MonthlyPrice.objects.filter(id=item_id).update(**item)
            #     updated_items.append(item_id)
            # else:
            #     MonthlyPrice.objects.create(**item)

        # delete not updated old records
        delete_ids = [item for item in old_items if item not in updated_items]
        MonthlyPrice.objects.filter(id__in=delete_ids).delete()
        instances = MonthlyPrice.objects.filter(property=property_id)
        serializer = MonthlyPriceItemSerializer(instances, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
