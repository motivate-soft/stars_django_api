from django.urls import path, include

from accommodation.views.property_view import update_images

urlpatterns = [
    path('property/', include('accommodation.urls.property')),
    path('category/', include('accommodation.urls.category')),
    path('amenity/', include('accommodation.urls.amenity')),
    path('pricing/', include('accommodation.urls.pricing')),
    path('booking/', include('accommodation.urls.booking')),
    path('update/', update_images),
]
