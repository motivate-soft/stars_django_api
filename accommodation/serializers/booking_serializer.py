from rest_framework import serializers


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


class BookingObjectSerializer(serializers.Serializer):

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
