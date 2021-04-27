from django.urls import path

from . import views

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog-list'),
    path('view/<slug>/', views.BlogDetailView.as_view(), name='blog-detail'),
]
