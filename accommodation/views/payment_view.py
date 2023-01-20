import logging
from json import dump

import requests
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from accommodation.views.paypal_client import PaypalClient
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest, OrdersAuthorizeRequest
from paypalhttp import HttpError

logger = logging.getLogger('django')

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+


class TokenCreateRequest:
    """
    Creates a Token.
    """

    def __init__(self):
        self.verb = "POST"
        self.path = "/v1/identity/generate-token"
        self.headers = {}
        self.headers["Content-Type"] = "application/json"
        self.body = None

    def prefer(self, prefer):
        self.headers["Prefer"] = str(prefer)

    def request_body(self, order):
        self.body = order
        return self


class PaypalRestAPI:
    def __init__(self):
        self.paypal_client = PaypalClient()

    def generate_client_token(self):
        token_request = TokenCreateRequest()
        token_request.prefer('return=representation')
        try:
            paypal_client = PaypalClient()

            response = paypal_client.execute(request=token_request)
            data = {
                "client_token": response.result.client_token,
                "expires_in": response.result.expires_in,
                # "id_token": response.result.id_token,
            }
            return data

        except IOError as ioe:
            logger.info("PaypalRestAPI Generate token ioe :>> %s" % ioe)

            if isinstance(ioe, HttpError):
                logger.info("PaypalRestAPI Generate token ioe.status_code :>> %s" % ioe.status_code)
            return Response(ioe)
        pass

    def create_order(self, amount, **kwargs):

        order_request = OrdersCreateRequest()
        order_request.prefer('return=representation')
        order_request.request_body(
            {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": "USD",
                            "value": amount
                        }
                    }
                ]
            }
        )
        try:
            response = self.paypal_client.execute(request=order_request)
            # logger.info("PaypalRestAPI Create Order :>> %s" % dump(response))
            data = {
                "id": response.result.id,
                "create_time": response.result.create_time,
                "intent": response.result.intent,
                "status": response.result.status,
            }
            return data

        except IOError as ioe:
            logger.info("PaypalRestAPI Create Order ioe :>> %s" % ioe)
            if isinstance(ioe, HttpError):
                logger.info("PaypalRestAPI Create Order ioe.status_code :>> %s" % ioe.status_code)
            return ioe
        pass

    def capture_order(self, order_id, **kwargs):

        order_request = OrdersCaptureRequest(order_id)
        order_request.prefer('return=representation')

        try:
            response = self.paypal_client.execute(request=order_request)
            logger.info("PaypalRestAPI Capture Order :>> %s" % response.result.id)
            links = [{"href": link.href, "method": link.method, "rel": link.rel} for link in response.result.links]
            # payment_source

            data = {
                "id": response.result.id,
                "create_time": response.result.create_time,
                "intent": response.result.intent,
                "links": links,
                "status": response.result.status,
            }
            return data

        except IOError as ioe:
            logger.info("PaypalRestAPI Capture Order ioe :>> %s" % ioe)
            if isinstance(ioe, HttpError):
                logger.info("PaypalRestAPI Capture Order ioe.status_code :>> %s" % ioe.status_code)
            return ioe
        pass
