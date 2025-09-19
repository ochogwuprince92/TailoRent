from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# Database (uses .env values from base.py)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": get_env_variable("DB_NAME"),
        "USER": get_env_variable("DB_USER"),
        "PASSWORD": get_env_variable("DB_PASSWORD"),
        "HOST": get_env_variable("DB_HOST", "localhost"),
        "PORT": get_env_variable("DB_PORT", "3306"),
    }
}

# Email backend for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

CORS_ALLOW_ALL_ORIGINS = True
