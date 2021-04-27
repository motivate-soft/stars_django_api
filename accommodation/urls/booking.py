from django.urls import path

from accommodation.views.booking_view import get_quote, AddPaymentAPIView

urlpatterns = [
    path('add_payment', AddPaymentAPIView.as_view()),
    path('get_quote', get_quote),
]
