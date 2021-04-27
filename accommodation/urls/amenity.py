from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accommodation.views.amenity_view import AmenityViewSet

router = DefaultRouter()
router.register('', AmenityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
