import copy

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment, requests
from django_api.settings.base import PAYPAL_SANDBOX_CLIENT_ID, PAYPAL_SANDBOX_CLIENT_SECRET, PAYPAL_LIVE_CLIENT_ID, \
    PAYPAL_LIVE_CLIENT_SECRET

http_proxy = "http://172.25.1.2:3129"
https_proxy = "http://172.25.1.2:3129"
ftp_proxy = "http://172.25.1.2:3129"

proxyDict = {
    "http": http_proxy,
    "https": https_proxy,
    "ftp": ftp_proxy
}


class PaypalClient(PayPalHttpClient):
    def __init__(self, env="development"):
        if env == "production":
            environment = LiveEnvironment(PAYPAL_LIVE_CLIENT_ID, PAYPAL_LIVE_CLIENT_SECRET)
        else:
            environment = SandboxEnvironment(PAYPAL_SANDBOX_CLIENT_ID, PAYPAL_SANDBOX_CLIENT_SECRET)
        PayPalHttpClient.__init__(self, environment)

    def execute(self, request):
        reqCpy = copy.deepcopy(request)

        try:
            getattr(reqCpy, 'headers')
        except AttributeError:
            reqCpy.headers = {}

        for injector in self._injectors:
            injector(reqCpy)

        data = None

        formatted_headers = self.format_headers(reqCpy.headers)

        if "user-agent" not in formatted_headers:
            reqCpy.headers["user-agent"] = self.get_user_agent()

        if hasattr(reqCpy, 'body') and reqCpy.body is not None:
            raw_headers = reqCpy.headers
            reqCpy.headers = formatted_headers
            data = self.encoder.serialize_request(reqCpy)
            reqCpy.headers = self.map_headers(raw_headers, formatted_headers)

        resp = requests.request(method=reqCpy.verb,
                                url=self.environment.base_url + reqCpy.path,
                                headers=reqCpy.headers,
                                data=data,
                                proxies=proxyDict)

        return self.parse_response(resp)
