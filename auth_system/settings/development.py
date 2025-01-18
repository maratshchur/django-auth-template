# settings/development.py
from .base import *
import os

DEBUG = True

ALLOWED_HOSTS = ['*'] 

DATABASES = {
		'default': {
      	'ENGINE': 'django.db.backends.postgresql',
      	'HOST' : os.environ.get('POSTGRES_HOST', 'localhost'),
      	'NAME': os.environ.get('POSTGRES_DB', 'auth'),
      	'USER': os.environ.get('POSTGRES_USER', 'postgres'),
      	'PASSWORD': os.environ.get('POSTGRES_PASSWORD', '1111'),
      	'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'root': {
#         'handlers': ['console'],
#         'level': 'DEBUG',
#     },
# }

CONSTANCE_CONFIG = {
    "ACCESS_TOKEN_LIFETIME": (30, "Access Token Lifetime in seconds"),
    "REFRESH_TOKEN_LIFETIME": (
        30 * 24 * 60 * 60,
        "Refresh Token Lifetime in seconds (default 30 days)",
    ),
}
