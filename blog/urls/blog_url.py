from django.urls import path

from blog.views.blog_view import BlogListCreateAPIView, BlogRetrieveUpdateDestroyAPIView, BlogListingAPIView, \
    BlogDetailAPIView

urlpatterns = [
    path('', BlogListCreateAPIView.as_view(), name='blog-list-create-view'),
    path('<int:pk>', BlogRetrieveUpdateDestroyAPIView.as_view(), name='blog-detail'),

    path('listing', BlogListingAPIView.as_view(), name='blog-list-create-view'),
    path('listing/<slug:slug>', BlogDetailAPIView.as_view(), name='blog-list-create-view'),
]
