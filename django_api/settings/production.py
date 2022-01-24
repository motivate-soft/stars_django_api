from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    ".localhost",
    "127.0.0.1",
    "starsofboston.com",
    "www.starsofboston.com",
    "starsofboston.org",
    "www.starsofboston.org",
    "starsofboston.net",
    "www.starsofboston.net",
]

CORS_ORIGIN_WHITELIST = [
    "http://18.117.1.73",
    "https://starsofboston.com",
    "https://www.starsofboston.com",
    "https://starsofboston.org",
    "https://www.starsofboston.org",
    "https://starsofboston.net",
    "https://www.starsofboston.net",
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
django-storages s3 setup
"""
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_REGION = "us-east-2"
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.amazonaws.com'
AWS_S3_CUSTOM_DOMAIN = 's3.us-east-2.amazonaws.com/starsofboston.com'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

"""
Email API setup
"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'  # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = env('SENDGRID_API_KEY')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{levelname} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'filename': 'log/django.log',
#             'when': 'midnight',  # this specifies the interval
#             'interval': 1,  # defaults to 1, only necessary for other values
#             'backupCount': 10,  # how many backup file to keep, 10 days
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }
