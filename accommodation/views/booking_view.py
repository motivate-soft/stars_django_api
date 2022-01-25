import logging
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
import xml.etree.ElementTree as et
import json

from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.views import APIView

from accommodation.models import Property, Price
from accommodation.models.price import MonthlyPrice
from accommodation.serializers.booking_serializer import BookingObjectSerializer
from accommodation.utils import get_add, get_payment, get_property_availability, get_quote


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
            return HttpResponse(json.dumps(valid_ser.errors), content_type="application/json",
                                status=HTTP_400_BAD_REQUEST)

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
                         rent=property_fee, cleaning_fee=cleaning_fee, total=total, net=property_fee, state_tax=tax,
                         add_items=add_items,
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
        date_paid = datetime.now().strftime('%Y-%m-%d %H:%M')

        get_payment(book_id=bkv_booking_id, pay_id=pay_id, date_paid=date_paid, amount=total,
                    operation='ADD', payment_type=payment_type, refund_portion=0, venue='Venue')
        get_payment(book_id=bkv_booking_id, pay_id=pay_id, date_paid=date_paid, amount=0,
                    operation='ADD', payment_type=payment_type, refund_portion=refundable_amount, venue='Venue')

        print('=========Add Payment API Response======\n', result)

        return {
            'status': 'ok',
            'booking_id': bkv_booking_id
        }


class BookingPricingView(APIView):
    permission_classes = []

    def get(self, request):
        property_id = self.request.query_params.get("property", None)
        checkin_date = self.request.query_params.get("checkin_date", None)
        checkout_date = self.request.query_params.get("checkout_date", None)
        adults = self.request.query_params.get("adults", None)
        children = self.request.query_params.get("children", None)

        property_instance = Property.objects.get(pk=property_id)
        if not property_id or not checkin_date or not checkout_date:
            raise ValidationError("Invalid data")
        if not property_instance:
            raise ValidationError({"property": "invalid"})

        # logger = logging.getLogger('django')
        # logger.log(0, "BookingPricingView")

        checkin_date = datetime.strptime(checkin_date, "%Y-%m-%d").date()
        checkout_date = datetime.strptime(checkout_date, "%Y-%m-%d").date()
        duration = (checkout_date + relativedelta(days=1) - checkin_date).days
        total_price = self.calc_daily_total(property_id=property_id, checkin_date=checkin_date,
                                            checkout_date=checkout_date)
        monthly_price = None
        monthly_discount = None
        if duration > 28:
            monthly_price = self.calc_monthly_total(property_id=property_id, checkin_date=checkin_date,
                                                    checkout_date=checkout_date)
            monthly_discount = total_price - monthly_price

        data = {
            'flat_price': float("{:.2f}".format(total_price)),
            'duration': duration,
        }
        if monthly_price:
            data['monthly_price'] = float("{:.2f}".format(monthly_price))
            data['monthly_discount'] = float("{:.2f}".format(monthly_discount))

        # try:
        #     response = get_quote(property_num=property_instance.bookerville_id, begin_date=checkin_date,
        #                          end_date=checkout_date, adults=adults, children=children)
        # except:
        #     logger = logging.getLogger('django')

        return Response(data=data)

    def calc_daily_total(self, property_id, checkin_date, checkout_date):
        query = Price.objects.filter(
            property=property_id
        ).filter(
            Q(start_date__range=[checkin_date, checkout_date]) | Q(end_date__range=[checkin_date, checkout_date])
        ).order_by('start_date')

        pricing_items = [item for item in query]
        property_instance = Property.objects.get(pk=property_id)

        total_price = 0
        duration = (checkout_date + relativedelta(days=1) - checkin_date).days

        if len(pricing_items) > 0:
            length = len(pricing_items)
            index = 0

            for pricing_item in pricing_items:
                start = pricing_item.start_date
                end = pricing_item.end_date
                if index == 0 and start < checkin_date:
                    start = checkin_date
                if index == length - 1 and end > checkout_date:
                    end = checkout_date
                pricing_duration = (end + relativedelta(days=1) - start).days
                total_price += pricing_item.price * pricing_duration
                duration -= pricing_duration
                index += 1

            if duration > 0:
                total_price += property_instance.price * duration
        else:
            total_price = property_instance.price * duration

        return total_price

    def calc_monthly_total(self, property_id, checkin_date, checkout_date):
        total_price = 0
        start = checkin_date
        while start < checkout_date:
            # start and end of month
            month_start = datetime(start.year, start.month, 1).date()
            month_end = month_start + relativedelta(months=1) - timedelta(days=1)
            # number of days in month
            n_month_days = (month_start + relativedelta(months=1) - month_start).days

            if checkout_date > month_end:
                c_month_days = (month_start + relativedelta(months=1) - start).days
                monthly_pricing = self.get_monthly_pricing(property_id=property_id, month_start=month_start)
                total_price += monthly_pricing * c_month_days / n_month_days
                start = month_end + timedelta(days=1)
            else:
                c_month_days = (checkout_date + timedelta(days=1) - start).days
                monthly_pricing = self.get_monthly_pricing(property_id=property_id, month_start=month_start)
                total_price += monthly_pricing * c_month_days / n_month_days
                start = month_end + timedelta(days=1)
        return total_price

    def get_monthly_pricing(self, property_id, month_start):
        pricing = MonthlyPrice.objects.filter(property=property_id, date=month_start).first()
        if pricing:
            return pricing.price
        else:
            property = Property.objects.get(pk=property_id)
            return property.min_month_price
