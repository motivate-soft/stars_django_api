from django.urls import path

from accommodation.views.booking_view import AddPaymentAPIView, BookingPricingView

urlpatterns = [
    path('add_payment', AddPaymentAPIView.as_view()),
    path('quote', BookingPricingView.as_view()),
]
