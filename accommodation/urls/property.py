from django.urls import path

from accommodation.views.property_view import PropertyListAPIView, PropertyDetailRetrieveAPIView, PropertyMapItemListAPIView, \
    AdminPropertyCreateAPIView, AdminPropertyRetrieveUpdateDestroyAPIView, AdminPropertyRetrieveUpdateDestroyBySlugAPIView, AdminPropertyListAPIView

urlpatterns = [
    #     Guest API
    path('listing', PropertyListAPIView.as_view()),
    path('locations', PropertyMapItemListAPIView.as_view()),
    path('listing/<slug:slug>', PropertyDetailRetrieveAPIView.as_view()),

    #     Admin API
    path('create', AdminPropertyCreateAPIView.as_view()),
    path('<int:pk>', AdminPropertyRetrieveUpdateDestroyAPIView.as_view()),
    path('<slug:slug>', AdminPropertyRetrieveUpdateDestroyBySlugAPIView.as_view()),
    path('', AdminPropertyListAPIView.as_view()),
]
