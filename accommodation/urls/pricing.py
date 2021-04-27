from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accommodation.views.pricing_view import PriceItemViewSet

router = DefaultRouter()
router.register(r'', PriceItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
