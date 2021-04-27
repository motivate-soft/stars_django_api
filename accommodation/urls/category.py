"""
modelViewSets 1
"""

from accommodation.views.category_view import CategoryViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', CategoryViewSet)
urlpatterns = [
    path('', include(router.urls)),
]

"""
modelViewSets 2
"""
# from rest_framework.urlpatterns import format_suffix_patterns
#
# from accommodation.views.category_view import CategoryViewSet
# from django.urls import path
#
#
# category_list = CategoryViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# category_detail = CategoryViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
# category_listing = CategoryViewSet.as_view({
#     'get': 'listing'
# })
#
# urlpatterns = format_suffix_patterns([
#     path('', category_list, name='category-list'),
#     path('<int:pk>/', category_detail, name='category-detail'),
#     path('list/', category_listing, name='category-listing'),
# ])

"""
Views
"""
# from django.urls import path
#
# from accommodation.views.category_view import CategoryListAPIView, CategoryCreateAPIView, CategoryRetrieveUpdateDestroyAPIView, CategoryItemsAPIView
#
# urlpatterns = [
#     path('create', CategoryCreateAPIView.as_view()),
#     path('<int:pk>', CategoryRetrieveUpdateDestroyAPIView.as_view()),
#     path('list', CategoryItemsAPIView.as_view()),
#     path('', CategoryListAPIView.as_view()),
# ]
