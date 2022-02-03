import logging
from urllib.request import Request, urlopen
from xml.etree import ElementTree
from bs4 import BeautifulSoup
from rest_framework import serializers

from django_api.settings.base import BOOKERVILLE_API_KEY

logger = logging.getLogger('django')


class BkvProperty:
    def __init__(self, property_id, account_id, last_update_date, detail_api_html=None):
        self.property_id = property_id  # The Bookerville property ID
        self.account_id = account_id  # The Bookerville account ID
        self.last_update_date = last_update_date  # The last update
        self.detail_api_html = detail_api_html  # The HTML access url

    def __str__(self):
        return self.property_id + " : " + self.account_id

    def __repr__(self):
        return self.property_id + " : " + self.account_id


# class BkvPropertySerializer(serializers.Serializer):
#     property_id = serializers.IntegerField()
#     account_id = serializers.IntegerField()
#     last_update_date = serializers.CharField()
#     detail_api_html = serializers.CharField()


def get_all_properties(auth_key=BOOKERVILLE_API_KEY):
    summary_string = 'https://www.bookerville.com/API-PropertySummary?s3cr3tK3y='
    request = summary_string + auth_key
    req = Request(request, headers={"Accept": "application/xml"})
    u = urlopen(req)
    tree = ElementTree.parse(u)
    root_elem = tree.getroot()
    prop_list = root_elem.findall("Property")

    if len(prop_list) <= 0:
        return None
    ret_val = []
    for child in prop_list:
        ret_val.append({
            "html_link": child.attrib['property_details_api_url'],
            "bkv_account": child.attrib['bkvAccountId'],
            "property_id": child.attrib['property_id'],
            "last_update": child.attrib['last_update'],
        })
    return ret_val


def get_quote(property_num, begin_date, end_date, adults=1, children=0, guest_email='', guest_address='',
              city='', state='', country='', first_name='', last_name='', phone='', zip='', company='', channel='',
              operation='QUOTE', auth_key=BOOKERVILLE_API_KEY):
    req_url = "https://www.bookerville.com/API-Booking?s3cr3tK3y=" + auth_key
    xml_string = "<operation>" + operation + "</operation><bkvPropertyId>" + str(
        property_num) + "</bkvPropertyId><beginDate>" + begin_date + "</beginDate><endDate>" + end_date + "</endDate><adults>" + str(
        adults) + "</adults><children>" + str(children) + "</children>"

    # Extra Data
    if company != '':
        xml_string += "<company>" + company + "</company>"
    if channel != '':
        xml_string += "<channel>" + channel + "</channel>"

    # Guest data
    guest_string = ''
    if guest_email != '':
        guest_string += "<email>" + guest_email + "</email>"
    if guest_address != '':
        guest_string += "<address>" + guest_address + "</address>"
    if city != '':
        guest_string += "<city>" + guest_address + "</city>"
    if state != '':
        guest_string += "<state>" + state + "</state>"
    if country != '':
        guest_string += "<country>" + country + "</country>"
    if first_name != '':
        guest_string += "<first_name>" + first_name + "</first_name>"
    if last_name != '':
        guest_string += "<last_name>" + last_name + "</last_name>"
    if guest_address != '':
        guest_string += "<address>" + guest_address + "</address>"
    if phone != '':
        guest_string += "<address>" + str(phone) + "</phone>"
    if zip != '':
        guest_string += "<zip>" + str(zip) + "</zip>"

    if guest_string != '':
        xml_string += '<guestData>' + guest_string + '</guestData>'

    xml_string = "<request>" + xml_string + "</request>"

    req = Request(url=req_url, data=xml_string.encode('utf-8'), headers={
        'Content-Type': 'application/xml'})
    response = urlopen(req)
    val = response.read()

    return val


def get_add(property_num, begin_date, end_date, adults, email, address, state, city, zip, country, first_name,
            last_name, phone, rent, cleaning_fee=0,
            total=0, child=0, company="Company", channel="Channel", guest_com="", over_oc=0, dis=0, net=0, state_tax=0,
            count_tax=0, prepayment=0,
            add_items=None, refund=0, operation="ADD", auth_key=BOOKERVILLE_API_KEY):
    req_url = "https://www.bookerville.com/API-Booking?s3cr3tK3y=" + auth_key
    xml_string = "<request> <operation>" + operation + "</operation> <bkvPropertyId>" + str(
        property_num) + "</bkvPropertyId> <address>" + address + "</address><state>" + state + "</state> <city>" + city + "</city> <company>" + company + "</company> <channel>" + channel + "</channel> <country>" + country + "</country> <email>" + email + "</email> <firstName>" + first_name + "</firstName> <lastName>" + last_name + "</lastName> <phone>" + phone + "</phone> <zip>" + str(
        zip) + "</zip> <beginDate>" + begin_date + "</beginDate> <endDate>" + end_date + "</endDate> <adults>" + str(
        adults) + "</adults> <children>" + str(
        child) + "</children> <guestComments>" + guest_com + "</guestComments> <rent>" + str(
        rent) + "</rent><cleaningFee>" + str(cleaning_fee) + "</cleaningFee><overOccupancySurcharge>" + str(
        over_oc) + "</overOccupancySurcharge> <discount>" + str(dis) + "</discount> <netRent>" + str(
        net) + "</netRent> <taxes> <tax> <id>1</id> <label>Tax1</label> <amount>" + str(
        state_tax) + "</amount> </tax> <tax> <id>2</id> <label>Tax2</label> <amount>" + str(
        count_tax) + "</amount> </tax> </taxes><total>" + str(
        total) + "</total><prePayment>" + str(prepayment) + "</prePayment><bookingStatus>Confirmed</bookingStatus>"

    # additionalItems should be a list of tuples
    xml_additions = "<additionalItems>"
    for item in add_items:
        xml_additions = xml_additions + "<additionalItem>" + "<label>" + \
                        item[0] + "</label> <amount>" + \
                        str(item[1]) + "</amount><taxed>" + item[2] + "</taxed>"
    xml_additions = xml_additions + "</additionalItems>"

    final = "<securityDeposit> <type>Refundable</type> <amount>" + \
            str(refund) + "</amount> </securityDeposit> <bookingURL></bookingURL> </request>"
    totalString = xml_string + xml_additions + final

    logger.info("Bookerville Utils :>> get_add %s" % totalString)

    req = Request(url=req_url, data=totalString.encode('utf-8'), headers={'Content-Type': 'application/xml'})
    response = urlopen(req)
    val = response.read()
    return val


def get_remove(bk_id, property_id, begin_date, end_date, operation='DELETE', auth_key=BOOKERVILLE_API_KEY):
    xml_string = "<request><operation>" + operation + "</operation><bkvBookingId>" + str(
        bk_id) + "</bkvBookingId><bkvPropertyId>" + str(
        property_id) + "</bkvPropertyId><begin_date>" + begin_date + "</begin_date><end_date>" + end_date + "</end_date></request>"
    req_url = "https://www.bookerville.com/API-Booking?s3cr3tK3y=" + auth_key
    req = Request(url=req_url, data=xml_string, headers={
        'Content-Type': 'application/xml'})
    response = urlopen(req)
    val = response.read()
    y = BeautifulSoup(val)
    return y


def get_payment(book_id, pay_id, date_paid, amount, operation='ADD', payment_type="Paypal", refund_portion=0,
                venue='Venue', auth_key=BOOKERVILLE_API_KEY):
    if operation != "Delete":
        pay_id = ""
    payment_string = "https://www.bookerville.com/API-Payment?s3cr3tK3y=" + auth_key
    xml_string = "<bookingPayment> <bkvBookingId>" + str(
        book_id) + "</bkvBookingId> <operation>" + operation + "</operation> <bkvBookingPaymentId>" + str(
        pay_id) + "</bkvBookingPaymentId> <datePaid>" + date_paid + "</datePaid> <type>" + payment_type + "</type> <amount>" + str(
        amount) + "</amount> <refundableSecurityDepositPortion>" + str(
        refund_portion) + "</refundableSecurityDepositPortion> <depositVenue>" + venue + "</depositVenue> </bookingPayment>"

    logger.info("Bookerville Utils :>> get_payment %s" % xml_string)

    req = Request(url=payment_string, data=xml_string.encode(
        'utf-8'), headers={'Content-Type': 'application/xml'})
    response = urlopen(req)
    val = response.read()
    # y = BeautifulSoup(val)
    return val


def get_property_availability(property_num, auth_key=BOOKERVILLE_API_KEY):
    property_string = 'https://www.bookerville.com/API-PropertyAvailability?s3cr3tK3y=' + \
                      auth_key + '&bkvPropertyId=' + str(property_num)
    req = Request(property_string, headers={"Accept": "application/xml"})
    u = urlopen(req)
    val = u.read()
    # with open('property_availability.xml', 'wb') as f:
    #     f.write(val)
    # y = BeautifulSoup(val)
    return val


def get_property_details(property_num, auth_key=BOOKERVILLE_API_KEY):
    property_string = 'https://www.bookerville.com/API-PropertyDetails?s3cr3tK3y=' + \
                      auth_key + '&bkvPropertyId=' + property_num
    req = Request(property_string, headers={"Accept": "application/xml"})
    u = urlopen(req)
    val = u.read()
    y = BeautifulSoup(val)
    return y


def get_multi_property_availability(checkin_date, checkout_date, adults, children=0, auth_key=BOOKERVILLE_API_KEY):
    xml = """
    <?xml version='1.0' encoding='utf-8'?>
    <request>
        <bkvAccountId>3077</bkvAccountId>
         <startDate>2020-10-05</startDate>
         <endDate>2020-10-07</endDate>
         <numAdults>2</numAdults>
         <numChildren>0</numChildren>
         <sendResultsAs>xml</sendResultsAs>
         <photoFullSize>Y</photoFullSize>
         <sortField>lastBooked</sortField>
         <sortOrder>ASC</sortOrder>
    </request>"""
    xml_payload = """
    <?xml version='1.0' encoding='utf-8'?>
    <request>
        <bkvAccountId>3077</bkvAccountId>
         <startDate>%s</startDate>
         <endDate>%s</endDate>
         <numAdults>%s</numAdults>
         <numChildren>%s</numChildren>
         <sendResultsAs>xml</sendResultsAs>
         <photoFullSize>Y</photoFullSize>
         <sortField>lastBooked</sortField>
         <sortOrder>ASC</sortOrder>
    </request>""" % (checkin_date, checkout_date, adults, children)
    print('===API request payload xml===\n', xml_payload)
    property_string = 'https://www.bookerville.com/API-Multi-Property-Availability-Search?s3cr3tK3y=' + auth_key
    req = Request(property_string, data=xml_payload.encode(
        'utf-8'), headers={"Accept": "application/xml", 'Content-Type': 'application/xml'})
    u = urlopen(req)
    val = u.read()

    return val
