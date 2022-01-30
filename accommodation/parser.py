import xmltodict
from django.conf import settings
from rest_framework.parsers import BaseParser
from rest_framework.exceptions import ParseError


class CustomXmlParser(BaseParser):
    """
    XML parser.
    """

    media_type = "application/xml"

    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        encoding = parser_context.get("encoding", settings.DEFAULT_CHARSET)
        try:
            data = xmltodict.parse(stream, attr_prefix='_', dict_constructor=dict)
        except:
            raise ParseError("XML parse error - %s")
        return data