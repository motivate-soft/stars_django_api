from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views.tag_view import TagViewSet, TagRetrieveAPIView

router = DefaultRouter()
router.register('', TagViewSet)

urlpatterns = [
    path('<slug:slug>', TagRetrieveAPIView.as_view(), name="tag-detail-by-slug"),
    path('', include(router.urls)),
]
