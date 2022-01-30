from django.urls import path

from accommodation.views.booking_view import BookingPricingView, BkvAddPaymentView, \
    BkvPropertyListingView

urlpatterns = [
    path('listing', BkvPropertyListingView.as_view()),
    path('add', BkvAddPaymentView.as_view()),
    path('quote', BookingPricingView.as_view()),
]
