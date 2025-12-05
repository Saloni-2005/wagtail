"""
Production settings for Render.com deployment
"""

import os
import dj_database_url
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Allow Render.com domain
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# Database - Use PostgreSQL on Render
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static files - WhiteNoise is already added in base.py
# MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Use the STORAGES setting from base.py (CompressedManifestStaticFilesStorage)
# But we need to relax strictness because of a missing Jcrop.gif in Wagtail 7.3a0
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        "OPTIONS": {
            "manifest_strict": False,
        },
    },
}

# Security settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# Wagtail settings
WAGTAILADMIN_BASE_URL = os.environ.get('WAGTAILADMIN_BASE_URL', 'https://your-app.onrender.com')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

try:
    from .local import *
except ImportError:
    pass
