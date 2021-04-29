"""
Django settings for django_api project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import pymysql
import os
import json
from datetime import timedelta
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'corsheaders',
    'rest_framework_simplejwt',
    'django_seed',
    'storages',
    'drf_yasg',

    # Local
    'authentication.apps.AuthenticationConfig',
    'users.apps.UsersConfig',
    'accommodation.apps.AccommodationConfig',
    'media.apps.MediaManagerConfig',
    'content.apps.ContentConfig',
    'blog.apps.BlogConfig'
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # django cors middleware
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'django_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'authentication/templates'),
                 os.path.join(BASE_DIR, 'users/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_api.wsgi.application'

pymysql.version_info = (1, 4, 6, 'final', 0)  # change mysqlclient version
pymysql.install_as_MySQLdb()

# [START db_setup]
if os.getenv('GAE_APPLICATION', None):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': env('DB_HOST'),
            'NAME': env('DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'NAME': 'starsofboston',
            'USER': 'admin',
            'PASSWORD': 'Admin123$',
        }
    }
# [END db_setup]

# Google Cloud Storage setup
if os.getenv('GAE_APPLICATION', None):
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = 'stars-website-react-2.appspot.com'

    from google.oauth2 import service_account

    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        os.path.join(BASE_DIR, 'credentials.json'))
    GS_EXPIRATION = timedelta(seconds=60)
    GS_DEFAULT_ACL = 'publicRead'

REST_FRAMEWORK = {
    # authentication
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.AllowAny'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
    # browserble API renderer
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DATE_INPUT_FORMATS': ['iso-8601', '%Y-%m-%dT%H:%M:%S.%fZ'],
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
}

# dj-rest-auth setting
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'token'
# JWT_AUTH_REFRESH_COOKIE = 'refresh-token'
OLD_PASSWORD_FIELD_ENABLED = True

REST_AUTH_SERIALIZERS = {
    'JWT_TOKEN_CLAIMS_SERIALIZER':
        'authentication.serializers.CustomTokenObtainPairSerializer',
    'USER_DETAILS_SERIALIZER':
        'authentication.serializers.CustomUserDetailsSerializer',
    'PASSWORD_RESET_SERIALIZER':
        'authentication.serializers.CustomPasswordResetSerializer',
}

# djangorestframework-simplejwt setting
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=300),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    # 'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

REST_SESSION_LOGIN = False
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_USERNAME_REQUIRED = True

DEFAULT_FROM_EMAIL = 'info@starsofboston.com'

DEFAULT_EMAIL_To = 'info@starsofboston.com'

AUTH_USER_MODEL = 'authentication.CustomUser'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = 'static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = 'static/media'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'frontend/build/static')]

BOOKERVILLE_API_KEY = env('BOOKERVILLE_API_KEY')
