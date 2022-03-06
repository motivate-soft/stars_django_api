from rest_framework import serializers
from accommodation.models.booking import Booking
from accommodation.serializers.property_serializer import AdminPropertyListItemSerializer


class BookingListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            '__all__'
        )

    property = AdminPropertyListItemSerializer()
    # guest = CustomUserDetailsSerializer()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    start = serializers.DateField()
    end = serializers.DateField()
    status = serializers.CharField(max_length=10)
    order_id = serializers.CharField(max_length=50)


class BookingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('__all__')

    def create(self, validated_data):
        instance = super(BookingDetailSerializer, self).create(validated_data)
        # save paypal order id
        return instance

    def update(self, instance, validated_data):
        # update status based on capture payment
        pass


class BillingObjectSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    country = serializers.CharField()
    state = serializers.CharField()
    city = serializers.CharField(allow_blank=True, allow_null=True)
    street = serializers.CharField()
    zip_code = serializers.CharField()


class GuestObjectSerializer(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    email = serializers.EmailField()
    phone_number = serializers.CharField(allow_null=True, allow_blank=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class BkvBookingSerializer(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    bookerville_id = serializers.IntegerField()
    checkin_date = serializers.DateField()
    checkout_date = serializers.DateField()
    adults = serializers.IntegerField()
    children = serializers.IntegerField(allow_null=True, default=0)
    property_fee = serializers.FloatField()
    cleaning_fee = serializers.FloatField()
    refundable_amount = serializers.FloatField()
    transaction_fee = serializers.FloatField()
    tax = serializers.FloatField()
    total = serializers.FloatField()

    guest = GuestObjectSerializer()
    billing = BillingObjectSerializer()


class BkvBookingQuoteSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    property = serializers.IntegerField()
    checkin_date = serializers.DateField()
    checkout_date = serializers.DateField()
    adults = serializers.IntegerField(required=False)
    children = serializers.IntegerField(required=False)
