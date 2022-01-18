from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accommodation.views.pricing_view import MonthlyPriceViewSet

router = DefaultRouter()
router.register(r'', MonthlyPriceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
