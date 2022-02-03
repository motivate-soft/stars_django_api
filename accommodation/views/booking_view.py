import logging
from datetime import datetime, timedelta
from urllib.error import HTTPError

import xmltodict
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
import xml.etree.ElementTree as et
import json

from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView

from accommodation.models import Property, Price
from accommodation.models.price import MonthlyPrice
from accommodation.serializers.booking_serializer import BookingObjectSerializer, BookingQuoteSerializer
from accommodation.utils import get_add, get_payment, get_property_availability, get_quote, get_all_properties

logger = logging.getLogger('django')


class BkvPropertyListingView(APIView):
    permission_classes = []

    def get(self, request):
        data = get_all_properties()
        return Response(data=data)


class BkvAddPaymentView(CreateAPIView):
    permission_classes = []
    serializer_class = BookingObjectSerializer

    def create(self, request, *args, **kwargs):
        booking_serializer = self.serializer_class(data=request.data)

        if not booking_serializer.is_valid():
            return Response(status=HTTP_400_BAD_REQUEST, data=booking_serializer.errors)

        data = booking_serializer.validated_data

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

        """
        Bookerville Add Booking
        """
        try:
            response = get_add(property_num=property_num, begin_date=begin_date, end_date=end_date, adults=adults,
                               child=children, address=street, state=state, city=city, zip=zip_code, country=country,
                               first_name=first_name, last_name=last_name, email=email, phone=phone,
                               rent=property_fee, cleaning_fee=cleaning_fee, total=total, net=property_fee,
                               state_tax=tax,
                               add_items=add_items, refund=refundable_amount, operation="ADD")
            response = str(response, "utf-8").replace("&", "&amp;")
            logger.info("BkvAddPaymentView :>> response %s" % response)

            data = xmltodict.parse(response, attr_prefix='_', dict_constructor=dict)
            response_data = data['BKV-API-Booking-Response']
            if response_data['status'] == 'success':
                booking_id = response_data['bkvBookingId']
                booking_confirm_code = response_data['confirmCode']
                booking_url = response_data['bkvBookingURL']
            elif response_data['status'] == 'failure':
                booking_error = response_data['error']
                return Response(data=booking_error, status=HTTP_400_BAD_REQUEST)
            else:
                return Response(data='Unknown error', status=HTTP_500_INTERNAL_SERVER_ERROR)
        except HTTPError as error:
            logger.error("BkvAddPaymentView :>> error %s" % error)
            return Response(data='Server error', status=HTTP_500_INTERNAL_SERVER_ERROR)

        payment_type = "Paypal"
        pay_id = ""
        date_paid = datetime.now().strftime('%Y-%m-%d %H:%M')

        """
        Bookerville Add Payment
        """
        try:
            get_payment(book_id=booking_id, pay_id=pay_id, date_paid=date_paid, amount=total,
                        operation='ADD', payment_type=payment_type, refund_portion=0, venue='Venue')
            get_payment(book_id=booking_id, pay_id=pay_id, date_paid=date_paid, amount=0,
                        operation='ADD', payment_type=payment_type, refund_portion=refundable_amount, venue='Venue')

            return Response(data={
                'booking_id': booking_id,
                'booking_confirm_code': booking_confirm_code,
                'booking_url': booking_url,
            })
        except HTTPError as error:
            logger.error("BkvAddPaymentView :>> error %s" % error)
            return Response(data='Server error', status=HTTP_500_INTERNAL_SERVER_ERROR)


class BookingPricingView(APIView):
    permission_classes = []

    def get(self, request):
        """
        Quote Validation
        """
        booking_quote_serializer = BookingQuoteSerializer(data=request.query_params)
        if not booking_quote_serializer.is_valid():
            return Response(status=HTTP_400_BAD_REQUEST, data=booking_quote_serializer.errors)

        property_id = booking_quote_serializer.validated_data['property']
        checkin_date = booking_quote_serializer.validated_data['checkin_date'].strftime("%Y-%m-%d")
        checkout_date = booking_quote_serializer.validated_data['checkout_date'].strftime("%Y-%m-%d")
        adults = booking_quote_serializer.validated_data.get("adults", None)
        children = booking_quote_serializer.validated_data.get("children", None)

        try:
            property_instance = Property.objects.get(pk=property_id)
        except Property.DoesNotExist:
            property_instance = None
        if not property_instance:
            raise ValidationError({"property": "invalid property id"})

        """
        Bookerville Quote API
        """
        booking_confirm_code = None
        try:
            response = get_quote(property_num=property_instance.bookerville_id, begin_date=checkin_date,
                                 end_date=checkout_date)
            response = str(response, "utf-8").replace("&", "&amp;")
            logger.info("BookingPricingView :>> response %s" % response)

            data = xmltodict.parse(response, attr_prefix='_', dict_constructor=dict)
            response_data = data['BKV-API-Booking-Response']
            if response_data['status'] == 'success':
                booking_confirm_code = response_data['confirmCode']
            elif response_data['status'] == 'failure':
                booking_error = response_data['error']
                return Response(data=booking_error, status=HTTP_400_BAD_REQUEST)
            else:
                return Response(data='Unknown error', status=HTTP_500_INTERNAL_SERVER_ERROR)
        except HTTPError as error:
            logger.error("BookingPricingView :>> error %s" % error)
            return Response(data='Server error', status=HTTP_500_INTERNAL_SERVER_ERROR)

        """
        Calculate Booking Price
        """
        checkin_date = datetime.strptime(checkin_date, "%Y-%m-%d").date()
        checkout_date = datetime.strptime(checkout_date, "%Y-%m-%d").date()
        duration = (checkout_date + relativedelta(days=1) - checkin_date).days
        nights_price = self.calc_daily_total(property_id=property_id, checkin_date=checkin_date,
                                             checkout_date=checkout_date)
        monthly_discount = 0
        if duration > 28:
            monthly_price = self.calc_monthly_total(property_id=property_id, checkin_date=checkin_date,
                                                    checkout_date=checkout_date)
            monthly_discount = nights_price - monthly_price

        accommodation_price = nights_price - monthly_discount
        tax = accommodation_price * property_instance.tax_rate / 100
        sub_total = accommodation_price + tax + +property_instance.cleaning_fee + property_instance.refundable_amount
        transaction_fee = sub_total * property_instance.transactionfee_rate / 100
        total = (1 + property_instance.transactionfee_rate / 100) * sub_total

        data = {
            'booking_confirm_code': booking_confirm_code,
            'nights': duration,
            'nights_price': float("{:.2f}".format(nights_price)),
            'monthly_discount': float("{:.2f}".format(monthly_discount)),
            'tax': float("{:.2f}".format(tax)),
            'transaction_fee': float("{:.2f}".format(transaction_fee)),
            'cleaning_fee': float("{:.2f}".format(property_instance.cleaning_fee)),
            'refundable_amount': float("{:.2f}".format(property_instance.refundable_amount)),
            'total': float("{:.2f}".format(total))
        }

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
