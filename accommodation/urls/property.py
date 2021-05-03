from django.urls import path

from accommodation.views.property_view import PropertyListAPIView, PropertyDetailRetrieveAPIView, \
    PropertyMapItemListAPIView, AdminPropertyRetrieveUpdateDestroyAPIView, \
    AdminPropertyRetrieveUpdateDestroyBySlugAPIView, AdminPropertyListCreateAPIView

urlpatterns = [
    #     Guest API
    path('listing', PropertyListAPIView.as_view()),
    path('locations', PropertyMapItemListAPIView.as_view()),
    path('listing/<slug:slug>', PropertyDetailRetrieveAPIView.as_view()),

    #     Admin API
    path('<int:pk>', AdminPropertyRetrieveUpdateDestroyAPIView.as_view()),
    path('<slug:slug>', AdminPropertyRetrieveUpdateDestroyBySlugAPIView.as_view()),
    path('', AdminPropertyListCreateAPIView.as_view()),
]
