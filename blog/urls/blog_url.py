from django.urls import path

from blog.views.blog_view import BlogListCreateAPIView, BlogRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', BlogListCreateAPIView.as_view(), name='blog-list-create-view'),
    path('<int:pk>', BlogRetrieveUpdateDestroyAPIView.as_view(), name='blog-detail'),
]
