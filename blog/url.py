from django.urls import path, include

urlpatterns = [
    path('tag/', include('blog.urls.tag_url')),
    path('post/', include('blog.urls.blog_url')),
]
