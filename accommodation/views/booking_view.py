import json
import logging
from datetime import datetime, timedelta
from urllib.error import HTTPError

import xmltodict
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action

from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
from rest_framework.views import APIView

from accommodation.models import Property, Price
from accommodation.models.booking import Booking
from accommodation.models.price import MonthlyPrice
from accommodation.serializers.booking_serializer import BkvBookingSerializer, BkvBookingQuoteSerializer, \
    BookingDetailSerializer, BookingListingSerializer
from accommodation.utils import get_add, get_payment, get_quote, get_all_properties

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from accommodation.views.payment_view import PaypalRestAPI
from accommodation.views.paypal_client import PaypalClient
from paypalcheckoutsdk.orders import OrdersCreateRequest
from paypalhttp import HttpError

logger = logging.getLogger('django')


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return BookingListingSerializer
        return BookingDetailSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'create':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class CreateClientTokenView(CreateAPIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        paypal_api = PaypalRestAPI()
        return Response(paypal_api.generate_client_token(), status=HTTP_201_CREATED)


class BookingOrderView(CreateAPIView):
    """
    Calculate booking price and Create paypal order.
    Returns paypal order detail.
    """
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # Validate request
        serializer = BkvBookingQuoteSerializer(data=request.data)
        serializer.is_valid()
        data = serializer.data
        if not serializer.is_valid():
            return Response(status=HTTP_400_BAD_REQUEST, data=serializer.errors)

        # Calculate booking price
        booking_pricing = BookingPricing(property_id=data['property'], checkin_date=data['checkin_date'],
                                         checkout_date=data['checkout_date'], adults=data['adults'])
        pricing = booking_pricing.calc_price()

        # Create paypal order
        paypal_api = PaypalRestAPI()
        return Response(paypal_api.create_order(pricing['total']), status=HTTP_201_CREATED)


class BookingApproveView(CreateAPIView):
    """
    Capture paypal order and update booking status.
    Add booking to Bookerville
    """
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # Validate request
        try:
            booking_instance = Booking.objects.get(pk=kwargs["pk"])
        except ObjectDoesNotExist:
            booking_instance = None

        if not booking_instance:
            raise ValidationError("can't find booking request")

        # Capture paypal payment order
        paypal_api = PaypalRestAPI()
        order_id = booking_instance.order_id
        paypal_response = paypal_api.capture_order(order_id)

        # Add booking to bookerville
        booking_pricing = BookingPricing(property_id=booking_instance.property.id,
                                         checkin_date=booking_instance.checkin_date.strftime("%Y-%m-%d"),
                                         checkout_date=booking_instance.checkout_date.strftime("%Y-%m-%d"),
                                         adults=booking_instance.adults)
        pricing = booking_pricing.calc_price()

        property_num = booking_instance.property.bookerville_id
        begin_date = booking_instance.checkin_date.strftime("%Y-%m-%d")
        end_date = booking_instance.checkout_date.strftime("%Y-%m-%d")
        adults = booking_instance.adults
        children = 0

        # {'nights': -41, 'nights_price': -6150.0, 'monthly_discount': 0.0, 'tax': -350.55, 'transaction_fee': -234.02,
        #  'cleaning_fee': 150.0, 'refundable_amount': 500.0, 'total': -6084.57}

        property_fee = pricing["property_fee"]
        cleaning_fee = pricing["cleaning_fee"]
        refundable_amount = pricing["refundable_amount"]
        transaction_fee = pricing["transaction_fee"]
        tax = pricing["tax"]
        subtotal = pricing["subtotal"]
        total = pricing["total"]

        first_name = booking_instance.first_name
        last_name = booking_instance.last_name
        email = booking_instance.email
        phone = booking_instance.phone_number

        country = booking_instance.country
        state = booking_instance.state
        city = booking_instance.city
        street = booking_instance.street
        zip_code = booking_instance.zip_code

        add_items = [
            ('Transaction Fee', transaction_fee, 'no'),
            ('Pre-Tax Subtotal', subtotal, 'no')
        ]

        try:
            response = get_add(property_num=property_num, begin_date=begin_date, end_date=end_date, adults=adults,
                               child=children, address=street, state=state, city=city, zip=zip_code, country=country,
                               first_name=first_name, last_name=last_name, email=email, phone=phone,
                               rent=property_fee, cleaning_fee=cleaning_fee, total=total, net=property_fee,
                               state_tax=tax,
                               add_items=add_items, refund=refundable_amount, operation="ADD")
            response = str(response, "utf-8").replace("&", "&amp;")
            logger.info("BookingApproveView :>> response %s" % response)

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
            logger.error("BookingApproveView :>> error %s" % error)
            return Response(data='Server error', status=HTTP_500_INTERNAL_SERVER_ERROR)

        payment_type = "PaypalRestAPI"
        pay_id = ""
        date_paid = paypal_response["create_time"].strftime('%Y-%m-%d %H:%M')

        try:
            get_payment(book_id=booking_id, pay_id=pay_id, date_paid=date_paid, amount=total,
                        operation='ADD', payment_type=payment_type, refund_portion=0, venue='Venue')
            get_payment(book_id=booking_id, pay_id=pay_id, date_paid=date_paid, amount=0,
                        operation='ADD', payment_type=payment_type, refund_portion=refundable_amount, venue='Venue')

            booking_instance.status = "A"
            # return Response({"id": paypal_api.capture_order(order_id)})
            #
            # return Response(data={
            #     'booking_id': booking_id,
            #     'booking_confirm_code': booking_confirm_code,
            #     'booking_url': booking_url,
            # })
            return Response(status=HTTP_200_OK)
        except HTTPError as error:
            logger.error("BkvAddPaymentView :>> error %s" % error)
            return Response(data='Server error', status=HTTP_500_INTERNAL_SERVER_ERROR)


class BkvPropertyListingView(APIView):
    permission_classes = []

    def get(self, request):
        data = get_all_properties()
        return Response(data=data)


class BkvAddPaymentView(CreateAPIView):
    permission_classes = []
    serializer_class = BkvBookingSerializer

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

        payment_type = "PaypalRestAPI"
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


class BkvQuoteView(APIView):
    """
    Calculate price and quote bookerville API.
    """
    permission_classes = []

    def get(self, request):
        # Validate quote request
        booking_quote_serializer = BkvBookingQuoteSerializer(data=request.query_params)
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

        # Booking quote API
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

        # Calculate price
        pricing_instance = BookingPricing(property_id=property_id, checkin_date=checkin_date,
                                          checkout_date=checkout_date, adults=adults, children=children)

        return Response(data=pricing_instance.calc_price(), status=HTTP_200_OK)


class BookingPricing:
    def __init__(self, property_id, checkin_date, checkout_date, adults, **kwargs):
        property_instance = Property.objects.get(pk=property_id)
        self.property_id = property_id
        self.property = property_instance
        self.checkin_date = checkin_date
        self.checkout_date = checkout_date
        self.adults = adults

        for key, value in kwargs.items():
            setattr(self, key, value)

    def calc_price(self):
        checkin_date = datetime.strptime(self.checkin_date, "%Y-%m-%d").date()
        checkout_date = datetime.strptime(self.checkout_date, "%Y-%m-%d").date()
        duration = (checkout_date + relativedelta(days=1) - checkin_date).days
        nights_price = self.calc_daily_total(property_id=self.property_id, checkin_date=checkin_date,
                                             checkout_date=checkout_date)
        monthly_discount = 0

        # apply monthly pricing for booking more than 28days
        if duration > 28:
            monthly_price = self.calc_monthly_total(property_id=self.property_id, checkin_date=checkin_date,
                                                    checkout_date=checkout_date)
            monthly_discount = nights_price - monthly_price

        accommodation_price = nights_price - monthly_discount
        tax = accommodation_price * self.property.tax_rate / 100
        sub_total = accommodation_price + tax + +self.property.cleaning_fee + self.property.refundable_amount
        transaction_fee = sub_total * self.property.transactionfee_rate / 100
        total = (1 + self.property.transactionfee_rate / 100) * sub_total

        data = {
            'nights': duration,
            'nights_price': float("{:.2f}".format(nights_price)),
            'monthly_discount': float("{:.2f}".format(monthly_discount)),
            'property_fee': float("{:.2f}".format(nights_price - monthly_discount)),
            'tax': float("{:.2f}".format(tax)),
            'transaction_fee': float("{:.2f}".format(transaction_fee)),
            'cleaning_fee': float("{:.2f}".format(self.property.cleaning_fee)),
            'refundable_amount': float("{:.2f}".format(self.property.refundable_amount)),
            'subtotal': float("{:.2f}".format(total - transaction_fee)),
            'total': float("{:.2f}".format(total))
        }

        return data

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
