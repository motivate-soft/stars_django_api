from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views.tag_view import TagViewSet

router = DefaultRouter()
router.register('', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
