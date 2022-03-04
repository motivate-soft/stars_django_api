import logging
from json import dump

import requests
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from accommodation.views.paypal_client import PaypalClient
from paypalcheckoutsdk.orders import OrdersCreateRequest
from paypalhttp import HttpError

logger = logging.getLogger('django')

http_proxy = "http://172.25.1.2:3129"
https_proxy = "http://172.25.1.2:3129"
ftp_proxy = "http://172.25.1.2:3129"

proxyDict = {
    "http": http_proxy,
    "https": https_proxy,
    "ftp": ftp_proxy
}

import paypalhttp


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




class Paypal:
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
                "id_token": response.result.id_token,
            }
            return data

        except IOError as ioe:
            logger.info("Paypal Create Order ioe :>> %s" % ioe)

            if isinstance(ioe, HttpError):
                logger.info("Paypal Create Order ioe.status_code :>> %s" % ioe.status_code)
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
        paypal_client = PaypalClient()
        try:
            response = paypal_client.execute(request=order_request)
            # logger.info("Paypal Create Order :>> %s" % dump(response))
            # print("Paypal Create Order :>> %s" % response)
            data = {
                "id": response.result.id,
                "create_time": response.result.create_time,
                "intent": response.result.intent,
                # "links": response.result.links,
                "status": response.result.status,
            }
            return Response(data)

        except IOError as ioe:
            logger.info("Paypal Create Order ioe :>> %s" % ioe)
            # print("Paypal Create Order ioe :>> %s" % ioe)
            # if isinstance(ioe, HttpError):
            #     # Something went wrong server-side
            #     logger.info("Paypal Create Order ioe.status_code :>> %s" % ioe.status_code)
            #     print("Paypal Create Order ioe.status_code :>> %s" % ioe.status_code)
            return Response(ioe)
        pass
