from django.urls import path, include

from media.views import MediaRetrieveUpdateDestroyAPIView, PaginatedMediaListView, MediaListCreateView

urlpatterns = [
    path('list', PaginatedMediaListView.as_view(), name='paginated_media_list_view'),

    path('<int:pk>', MediaRetrieveUpdateDestroyAPIView.as_view(), name='media_detail_view'),
    path('', MediaListCreateView.as_view(), name='property_media_list_view'),
]
