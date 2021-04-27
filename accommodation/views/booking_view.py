import datetime
from django.http import JsonResponse, HttpResponse
import xml.etree.ElementTree as et

import json

from rest_framework.generics import CreateAPIView
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from accommodation.serializers.booking_serializer import BookingObjectSerializer
from accommodation.utils import get_add, get_payment, get_property_availability


class AddPaymentAPIView(CreateAPIView):
    serializer_class = BookingObjectSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        valid_ser = self.serializer_class(data=request.data)

        if valid_ser.is_valid():
            res = self.add_payment(valid_ser.validated_data)
            if res['status'] == 'ok':
                return JsonResponse(data={'booking_id': res['booking_id']}, safe=True, status=HTTP_201_CREATED)
            else:
                return JsonResponse(data={'error': res['error']}, safe=True, status=HTTP_400_BAD_REQUEST)
        else:
            print('valid_ser.errors', valid_ser.errors)
            return HttpResponse(json.dumps(valid_ser.errors), content_type="application/json", status=HTTP_400_BAD_REQUEST)

    @staticmethod
    def add_payment(data):
        property_num = data["bookerville_id"]
        begin_date = data["checkin_date"].strftime("%Y-%m-%d")
        end_date = data["checkout_date"].strftime("%Y-%m-%d")
        adults = data["adults"]
        children = data["children"]
        property_fee = data["property_fee"]
        cleaning_fee = data["cleaning_fee"]
        refundable_amount = data["refundable_amount"]
        transaction_fee = data["transaction_fee"]
        tax = data["tax"]
        total = data["total"]

        first_name = data["guest"]["first_name"]
        last_name = data["guest"]["last_name"]
        email = data["guest"]["email"]
        phone = data["guest"]["phone_number"]

        country = data["billing"]["country"]
        state = data["billing"]["state"]
        city = data["billing"]["city"]
        street = data["billing"]["street"]
        zip_code = data["billing"]["zip_code"]

        add_items = [
            ('Transaction Fee', transaction_fee, 'no'),
            ('Pre-Tax Subtotal', total - transaction_fee, 'no')
        ]

        # add booking API
        result = get_add(property_num=property_num, begin_date=begin_date, end_date=end_date, adults=adults,
                         child=children, address=street, state=state, city=city, zip=zip_code, country=country,
                         first_name=first_name, last_name=last_name, email=email, phone=phone,
                         rent=property_fee, cleaning_fee=cleaning_fee, total=total, net=property_fee, state_tax=tax, add_items=add_items,
                         refund=refundable_amount, operation="ADD")

        print('=========Add Booking API Response======\n', result)
        root = et.fromstring(result)
        book_id = [e.text for e in root.findall('bkvBookingId')]

        if len(book_id) > 0:
            bkv_booking_id = book_id[0]
        else:
            error = [e.text for e in root.findall('error')]
            return {
                'status': 'failed',
                'error': error[0]
            }

        # add payment API
        payment_type = "Paypal"
        pay_id = ""
        date_paid = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        get_payment(book_id=bkv_booking_id, pay_id=pay_id, date_paid=date_paid, amount=total,
                    operation='ADD', payment_type=payment_type, refund_portion=0, venue='Venue')
        get_payment(book_id=bkv_booking_id, pay_id=pay_id, date_paid=date_paid, amount=0,
                    operation='ADD', payment_type=payment_type, refund_portion=refundable_amount, venue='Venue')

        print('=========Add Booking API Response======\n', result)

        return {
            'status': 'ok',
            'booking_id': bkv_booking_id
        }


def get_quote(request):
    if request.method == 'POST':
        booking_data = json.loads(request.body)
        property_num = booking_data["bookerville_id"]
        begin_date = datetime.datetime.strftime(booking_data["checkin_date"], "%Y-%M-%D")
        end_date = datetime.datetime.strftime(booking_data["checkout_date"], "%Y-%M-%D")
        result = get_property_availability(property_num)
        root = et.fromstring(result)

        arrival_dates = [e.text for e in root.findall('BookedStays/BookedStay//ArrivalDate')]
        departure_dates = [e.text for e in root.findall('BookedStays/BookedStay//DepartureDate')]
        for key, arrival_date in enumerate(arrival_dates):
            if arrival_date <= begin_date <= departure_dates[key] or arrival_date <= end_date <= departure_dates[key]:
                return JsonResponse({'status': 'not available'})

        return JsonResponse({'status': 'available'})
