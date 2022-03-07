from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accommodation.views.booking_view import BkvQuoteView, BkvAddPaymentView, \
    BkvPropertyListingView, BookingViewSet, BookingOrderView, CreateClientTokenView, BookingApproveView

router = DefaultRouter()
router.register(r'', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('token', CreateClientTokenView.as_view()),
    path('quote', BkvQuoteView.as_view()),
    path('order', BookingOrderView.as_view()),

    path('<int:pk>/approve', BookingApproveView.as_view()),
    path('<int:pk>/decline', BookingApproveView.as_view()),
    path('listing', BkvPropertyListingView.as_view()),
    path('add', BkvAddPaymentView.as_view()),
]
