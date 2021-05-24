from django.urls import path, include
from rest_framework.routers import DefaultRouter

from django_meta.views import MetaViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'', MetaViewSet)
user_detail = MetaViewSet.as_view({
    'get': 'retrieve'
})
urlpatterns = [
    path('', include(router.urls)),
]
