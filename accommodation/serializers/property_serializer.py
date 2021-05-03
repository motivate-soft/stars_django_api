import datetime

from rest_framework import serializers
import xml.etree.ElementTree as et

from accommodation.models import Property, Room, Amenity, Price
from accommodation.serializers.amenity_serializer import AmenitySerializer, AmenityListingSerializer
from accommodation.serializers.price_serializer import PriceItemSerializer
from accommodation.serializers.room_serializer import RoomSerializer, RoomDetailSerializer
from accommodation.utils import get_property_availability
from media.models import Media
from media.serializer import MediaSerializer, PropertyMediaSerializer

"""
Guest View Serializer
"""


class PropertyListingItemSerializer(serializers.ModelSerializer):
    featured_img = PropertyMediaSerializer(read_only=True)
    category = serializers.StringRelatedField()

    class Meta:
        model = Property
        fields = (
            'id', 'name', 'category', 'slug', 'price', 'min_price', 'min_month_price',
            'bedroom_count', 'bathroom_count', 'shared_bathroom', 'sleeps', 'min_sleeps',
            'cleaning_fee', 'transactionfee_rate', 'tax_rate', 'refundable_amount',
            'tour360', 'furnished', 'rental_parking', 'pets_considered', 'featured_img'
        )


class PropertyMapItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            'id', 'name', 'address', 'slug', 'lat', 'lng'
        )


class PropertyDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    property_rooms = RoomDetailSerializer(many=True, read_only=True)
    # pricing_items = PriceItemSerializer(many=True, read_only=True)
    pricing_items = serializers.SerializerMethodField('get_pricing_items')
    amenities = AmenityListingSerializer(many=True, required=False, read_only=True)
    featured_img = PropertyMediaSerializer(required=False, read_only=True)
    gallery_imgs = PropertyMediaSerializer(many=True, required=False, read_only=True)
    similar_properties = PropertyListingItemSerializer(many=True, required=False, read_only=True)
    # gallery_imgs = serializers.SerializerMethodField('get_gallery_images')
    # similar_properties = serializers.SerializerMethodField('get_similar_properties')
    checked_dates = serializers.SerializerMethodField('get_checked_dates')

    class Meta:
        model = Property
        fields = (
            'id', 'name', 'slug',
            'bookerville_id', 'category',
            'checked_dates',
            'description', 'neighbourhood', 'transit', 'lat', 'lng',
            'bedroom_count', 'bathroom_count', 'shared_bathroom',
            'sleeps', 'min_sleeps',
            'price', 'min_price', 'min_month_price', 'pricing_items', 'cleaning_fee',
            'transactionfee_rate',
            'tax_rate',
            'refundable_amount',
            'furnished', 'rental_parking', 'pets_considered',
            'property_rooms', 'amenities', 'tour360',
            'featured_img', 'gallery_imgs', 'similar_properties', 'created_date', 'updated_date'
        )
        lookup_field = 'slug'

    @staticmethod
    def get_similar_properties(obj):
        properties = Property.objects.filter(category=obj.category).exclude(id=obj.id).order_by('created_date')[:5]
        serializer = PropertyListingItemSerializer(properties, many=True)
        return serializer.data

    @staticmethod
    def get_checked_dates(obj):
        checked_dates = []
        result = get_property_availability(obj.bookerville_id)
        root = et.fromstring(result)

        arrival_dates = [e.text for e in root.findall('BookedStays/BookedStay//ArrivalDate')]
        departure_dates = [e.text for e in root.findall('BookedStays/BookedStay//DepartureDate')]
        for key, arrival_date in enumerate(arrival_dates):
            print('arrival_dates', datetime.datetime.strptime(arrival_date, "%Y-%m-%d"), key, arrival_date,
                  departure_dates[key])
            checked_dates.append({
                'arrival_date': arrival_date,
                'departure_date': departure_dates[key],
            })

        return checked_dates

    @staticmethod
    def get_gallery_images(obj):
        return PropertyMediaSerializer(obj.gallery_imgs.all().order_by('order'), many=True).data

    @staticmethod
    def get_pricing_items(obj):
        return PriceItemSerializer(Price.objects.filter(property=obj.id, end_date__gte=datetime.datetime.now()),
                                   many=True, read_only=True).data


"""
Admin View Serializer
"""


class AdminPropertyListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            'id', 'slug', 'name', 'address', 'bookerville_id', 'updated_date'
        )


# Property detail
class AdminPropertyDetailSerializer(serializers.ModelSerializer):
    property_rooms = RoomSerializer(many=True)
    # amenities = AmenitySerializer(many=True, required=False, read_only=True)
    gallery_imgs = MediaSerializer(many=True, required=False, read_only=True)
    featured_img = MediaSerializer(required=False, read_only=True)

    class Meta:
        model = Property
        fields = (
            'id', 'bookerville_id', 'name', 'category', 'address', 'slug', 'description', 'neighbourhood', 'transit',
            'furnished', 'rental_parking', 'pets_considered',
            'lat', 'lng',
            'price', 'min_price', 'min_month_price',
            'bedroom_count', 'bathroom_count', 'shared_bathroom', 'sleeps', 'min_sleeps',
            'property_rooms', 'amenities',
            'cleaning_fee', 'transactionfee_rate', 'tax_rate', 'refundable_amount',
            'tour360', 'featured_img', 'gallery_imgs', 'similar_properties', 'created_date', 'updated_date'
        )

    def create(self, validated_data):
        if 'property_rooms' in validated_data.keys():
            validated_data.pop('property_rooms')
        if 'similar_properties' in validated_data.keys():
            validated_data.pop('similar_properties')
        if 'amenities' in validated_data.keys():
            validated_data.pop('amenities')

        instance = Property.objects.create(**validated_data)

        request = self.context['request']
        amenities = request.data.get('amenities', [])
        featured_img = request.data.get('featured_img', None)
        gallery_imgs = request.data.get('gallery_imgs', [])
        rooms_data = request.data.get('property_rooms', [])
        similar_properties = request.data.get('similar_properties', [])

        if featured_img is not None:
            image = Media.objects.filter(pk=featured_img)[:1].get()
            instance.featured_img = image

        # Set property's gallery images
        if gallery_imgs:
            order = 1

            for image_id in gallery_imgs:
                Media.objects.filter(pk=image_id).update(order=order)
                order += 1

            images = Media.objects.filter(id__in=gallery_imgs)
            instance.gallery_imgs.set(images)

        # Set property's similar properties
        if similar_properties:
            properties = Property.objects.filter(id__in=similar_properties)
            instance.similar_properties.set(properties)

        # Set property's rooms
        for room_data in rooms_data:
            Room.objects.create(property=instance, **room_data)

        if amenities:
            amenities = Amenity.objects.filter(pk__in=amenities)
            instance.amenities.set(amenities)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        if 'property_rooms' in validated_data.keys():
            validated_data.pop('property_rooms')
        if 'similar_properties' in validated_data.keys():
            validated_data.pop('similar_properties')
        if 'amenities' in validated_data.keys():
            validated_data.pop('amenities')

        instance = super(AdminPropertyDetailSerializer, self).update(instance, validated_data)

        request = self.context['request']
        amenities = request.data.get('amenities', [])
        featured_img = request.data.get('featured_img', None)
        gallery_imgs = request.data.get('gallery_imgs', [])
        rooms_data = request.data.get('property_rooms', [])
        similar_properties = request.data.get('similar_properties', [])

        print("++++update extra fields++++", amenities, featured_img, gallery_imgs, similar_properties)
        # Update property's featured image
        if featured_img is not None:
            image = Media.objects.filter(pk=featured_img)[:1].get()
            instance.featured_img = image

        # Update property's gallery images

        if gallery_imgs:
            order = 1

            for image_id in gallery_imgs:
                Media.objects.filter(pk=image_id).update(order=order)
                order += 1

            images = Media.objects.filter(id__in=gallery_imgs)
            instance.gallery_imgs.set(images)

        if similar_properties:
            properties = Property.objects.filter(id__in=similar_properties)
            instance.similar_properties.set(properties)
            # Set property's rooms

        for room_data in rooms_data:
            # existing room
            if 'id' in room_data.keys():
                # Delete room which doesn't have name and bed type
                if room_data["name"] == "" and room_data["bed_type"] == "":
                    Room.objects.filter(id=room_data["id"]).delete()
                Room.objects.filter(id=room_data["id"]).update(name=room_data["name"], bed_type=room_data["bed_type"])
            else:
                Room.objects.create(property=instance, **room_data)

        if amenities:
            amenities = Amenity.objects.filter(pk__in=amenities)
            instance.amenities.set(amenities)
        instance.amenities.set(amenities)

        instance.save()
        return instance

    # def get_amenity_ids(self, obj):
    #     amenity_ids = obj.amenities.all().values_list('id', flat=True).order_by('id')
    #     # Ids = obj.amenities.all().values('id')
    #     print(obj.amenities.all().values_list('id', flat=True).order_by('id'))
    #     return amenity_ids
