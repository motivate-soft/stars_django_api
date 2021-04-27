from django.urls import path, include
from rest_auth import views

from authentication.views.custom_token_view import CustomTokenObtainPairView, CustomTokenRefreshView, \
    LogoutAndBlacklistRefreshTokenForUserView

urlpatterns = [
    path('token/obtain/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='refresh_token'),
    path('token/blacklist/', LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='blacklist'),
    # Override django-rest-auth login url
    # url(r'^rest-auth/login/$', TokenObtainPairView.as_view(), name='rest_login'),
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
    path('rest-auth/password/reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
]
