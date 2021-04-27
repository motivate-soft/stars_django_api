from django.urls import path

from users.views import UserListView, UserRetrieveUpdateDestroyView, CustomUserCreate, send_contact_email, send_apply_email

urlpatterns = [
    # path('create/', UserCreateView.as_view()),
    path('create', CustomUserCreate.as_view()),
    path('<int:pk>', UserRetrieveUpdateDestroyView.as_view()),
    path('contact_email', send_contact_email),
    path('apply_email', send_apply_email),
    path('', UserListView.as_view()),
]
