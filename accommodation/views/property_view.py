from urllib.parse import parse_qs
import urllib.parse as urlparse

import xml.etree.ElementTree as et

from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListCreateAPIView

from accommodation.models import Category
from accommodation.models.property import Property
from accommodation.serializers.property_serializer import PropertyDetailSerializer, PropertyListingItemSerializer, \
    PropertyMapItemSerializer, AdminPropertyListItemSerializer, AdminPropertyDetailSerializer
from accommodation.utils import get_multi_property_availability

"""
Guest View
"""


# Guest page property list view
class PropertyListAPIView(ListAPIView):
    serializer_class = PropertyListingItemSerializer
    permission_classes = []

    def get_queryset(self):
        category_slug = self.request.query_params.get('category', None)
        checkin_date = self.request.query_params.get('checkin_date', None)
        checkout_date = self.request.query_params.get('checkout_date', None)
        adults = self.request.query_params.get('adults', None)
        children = self.request.query_params.get('children', None)

        queryset = Property.objects.all()

        if checkin_date is not None and checkout_date is not None and adults is not None:
            if not children or children is None:
                children = 0
            property_ids = []
            result = get_multi_property_availability(checkin_date=checkin_date, checkout_date=checkout_date,
                                                     adults=str(adults), children=str(children))
            root = et.fromstring(result)
            booking_target_urls = [e.text for e in root.findall('MultiPropertySearchResult//bookingTargetURL')]
            for key, url in enumerate(booking_target_urls):
                parsed_url = urlparse.urlparse(url)
                property_ids.append(int(parse_qs(parsed_url.query)['property'][0]))
            queryset = queryset.filter(bookerville_id__in=property_ids)

        if category_slug is not None:
            category = Category.objects.get(slug=category_slug)

            if category is not None:
                queryset = queryset.filter(category=category.id)

        return queryset


# Guest page location map list view
class PropertyMapItemListAPIView(ListAPIView):
    serializer_class = PropertyMapItemSerializer
    permission_classes = []
    queryset = Property.objects.all()


# Guest page property detail view
class PropertyDetailRetrieveAPIView(RetrieveAPIView):
    permission_classes = []
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializer
    lookup_field = 'slug'


"""
Admin View
"""


class AdminPropertyListCreateAPIView(ListCreateAPIView):
    queryset = Property.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdminPropertyDetailSerializer
        return AdminPropertyListItemSerializer


class AdminPropertyRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = AdminPropertyDetailSerializer


class AdminPropertyRetrieveUpdateDestroyBySlugAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = AdminPropertyDetailSerializer
    lookup_field = 'slug'
