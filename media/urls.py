from django.urls import path, include

from media.views import MediaCreateView, PropertyMediaListView, MediaRetrieveUpdateDestroyAPIView, MediaMultipleUpdate, PaginatedMediaListView

urlpatterns = [
    # Bulk Update image order
    path('update', MediaMultipleUpdate.as_view(), name='mutiple_media_update_view'),
    # Create/Retrieve/Update
    path('create', MediaCreateView.as_view(), name='media_create_view'),
    path('<int:pk>', MediaRetrieveUpdateDestroyAPIView.as_view(), name='media_detail_view'),
    # Paginated List
    path('list', PaginatedMediaListView.as_view(), name='paginated_media_list_view'),
    path('', PropertyMediaListView.as_view(), name='property_media_list_view'),
]
