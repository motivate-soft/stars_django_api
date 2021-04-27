from django.urls import path, include

urlpatterns = [
    path('property/', include('accommodation.urls.property')),
    path('category/', include('accommodation.urls.category')),
    path('amenity/', include('accommodation.urls.amenity')),
    path('pricing/', include('accommodation.urls.pricing')),
    path('booking/', include('accommodation.urls.booking')),
]
