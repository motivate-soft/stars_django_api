from django.urls import path, include

from media.views import MediaRetrieveUpdateDestroyAPIView, MediaMultipleUpdate, \
    PaginatedMediaListView, MediaListCreateView

urlpatterns = [
    # Bulk Update image order
    path('update', MediaMultipleUpdate.as_view(), name='mutiple_media_update_view'),

    path('<int:pk>', MediaRetrieveUpdateDestroyAPIView.as_view(), name='media_detail_view'),
    path('list', PaginatedMediaListView.as_view(), name='paginated_media_list_view'),
    path('', MediaListCreateView.as_view(), name='property_media_list_view'),
]
