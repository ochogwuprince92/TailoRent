from .base import *

DEBUG = False

ALLOWED_HOSTS = get_env_variable("ALLOWED_HOSTS").split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": get_env_variable("DB_NAME"),
        "USER": get_env_variable("DB_USER"),
        "PASSWORD": get_env_variable("DB_PASSWORD"),
        "HOST": get_env_variable("DB_HOST"),
        "PORT": get_env_variable("DB_PORT", "3306"),
    }
}

# Email backend (SendGrid via Anymail)
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
DEFAULT_FROM_EMAIL = get_env_variable("DEFAULT_FROM_EMAIL")

# Static files (served by whitenoise or web server)
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media
MEDIA_ROOT = BASE_DIR / "media"

# Security (keep as you already had)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
