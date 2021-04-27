import datetime
from rest_framework import serializers
from accommodation.models import Price, Property


def decrement_date(date, days=1):
    print('date', date)
    date = datetime.datetime.strptime(str(date), "%Y-%m-%d")
    new_date = date - datetime.timedelta(days=days)
    return new_date.strftime("%Y-%m-%d")


def increment_date(date, days=1):
    print('date', date)
    date = datetime.datetime.strptime(str(date), "%Y-%m-%d")
    new_date = date + datetime.timedelta(days=days)
    return new_date.strftime("%Y-%m-%d")


class PriceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = (
            'id', 'price', 'start_date', 'end_date', 'property'
        )
        extra_kwargs = {'id': {'read_only': False, 'required': False}}

    def create(self, validated_data):
        qstart_date = validated_data['start_date']
        qend_date = validated_data['end_date']
        print('qstart_date, qend_date', qstart_date, qend_date, decrement_date(qstart_date))

        # update item with date range involving new item's date range
        if len(Price.objects.filter(start_date__lt=qstart_date, end_date__gt=qend_date)) > 0:
            item = Price.objects.filter(start_date__lt=qstart_date, end_date__gt=qend_date)[0]
            Price.objects.create(start_date=increment_date(qend_date), end_date=item.end_date, price=item.price, property=item.property)
            item.end_date = decrement_date(qstart_date)
            item.save()

        # delete item in date range
        Price.objects.filter(start_date__gte=qstart_date, end_date__lte=qend_date).delete()

        # update item with end_date in new item's date range
        Price.objects.filter(start_date__lt=qstart_date).filter(end_date__gte=qstart_date, end_date__lte=qend_date).update(
            end_date=decrement_date(qstart_date))

        # update item with start_date in new item's date range
        Price.objects.filter(start_date__gte=qstart_date, start_date__lte=qend_date).filter(end_date__gt=qend_date).update(
            start_date=increment_date(qend_date))
        instance = Price.objects.create(**validated_data)

        if validated_data["price"] == validated_data["property"].price:
            # When price is same with default price, delete created pricing item
            Price.objects.get(pk=instance.id).delete()

        return instance
