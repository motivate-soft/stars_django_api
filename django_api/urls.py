from dj_rest_auth.views import PasswordResetConfirmView
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='API Docs',
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # this url is used to generate email content
    path('reset-password/<token>/<uidb64>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('api/rest-auth/', include('dj_rest_auth.urls')),
    path('api/rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/account/', include('allauth.urls')),

    path('api/users/', include('users.urls')),
    path('api/accommodation/', include('accommodation.url')),
    path('api/media/', include('media.urls')),
    path('api/content/', include('content.urls')),
    path('api/blog/', include('blog.url')),
    path('api/meta/', include('django_meta.urls')),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api_docs')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
