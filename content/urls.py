from django.urls import path
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny

from content.views import ContentCreate, ContentRetrieveUpdateDestroyAPIView, ContentListView

urlpatterns = [
    path('create', ContentCreate.as_view()),
    path('<int:pk>', ContentRetrieveUpdateDestroyAPIView.as_view()),
    path('', authentication_classes([])(permission_classes([AllowAny])(ContentListView)).as_view()),
]
