from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

# ALLOWED_HOSTS = [
#     ".localhost",
#     "127.0.0.1",
#     "starsofboston.com",
#     "www.starsofboston.com",
#     "starsofboston.org",
#     "www.starsofboston.org",
#     "starsofboston.net",
#     "www.starsofboston.net",
# ]

CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "https://localhost:3000",

    "http://starsofboston.com",
    "http://www.starsofboston.com",
    "http://starsofboston.org",
    "http://www.starsofboston.org",
    "http://starsofboston.net",
    "http://www.starsofboston.net",

    "https://starsofboston.com",
    "https://www.starsofboston.com",
    "https://starsofboston.org",
    "https://www.starsofboston.org",
    "https://starsofboston.net",
    "https://www.starsofboston.net"
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': env('DB_HOST'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

"""
Email API setup
"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'  # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = env('SENDGRID_API_KEY')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
