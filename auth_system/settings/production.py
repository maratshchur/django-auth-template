from .base import *
import dj_database_url

DEBUG = False  

ALLOWED_HOSTS = ["auth-temp-48821ad5a163.herokuapp.com", "127.0.0.1"]


DATABASES = {
    "default": dj_database_url.config(default="postgres://localhost")
}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


CONSTANCE_CONFIG = {
    "ACCESS_TOKEN_LIFETIME": (30, "Access Token Lifetime in seconds"),
    "REFRESH_TOKEN_LIFETIME": (
        30 * 24 * 60 * 60,
        "Refresh Token Lifetime in seconds (default 30 days)",
    ),
}
