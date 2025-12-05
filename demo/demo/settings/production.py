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

from whitenoise.storage import CompressedManifestStaticFilesStorage, MissingFileError

class NonStrictCompressedManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    """
    Custom storage that handles missing files gracefully and ensures proper URL resolution
    """
    manifest_strict = False
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Force manifest loading
        self.load_manifest()
    
    def hashed_name(self, name, content=None, filename=None):
        try:
            result = super().hashed_name(name, content, filename)
            return result
        except (ValueError, MissingFileError) as e:
            # Suppress errors for missing files referenced in CSS
            # This allows collectstatic to complete even if some referenced files are missing
            print(f"Warning: Missing file {name}, using original name: {e}")
            return name
    
    def url(self, name, force=False):
        """
        Ensure URLs are properly resolved through the manifest
        """
        try:
            # Force manifest loading if not already loaded
            if not hasattr(self, '_manifest'):
                self.load_manifest()
            
            result = super().url(name, force)
            return result
        except (ValueError, MissingFileError) as e:
            print(f"Warning: Could not resolve URL for {name}: {e}")
            # Fallback to basic URL construction
            return self.base_url + name
    
    def stored_name(self, name):
        """
        Override to ensure proper manifest lookup
        """
        try:
            return super().stored_name(name)
        except (ValueError, MissingFileError):
            return name

# Use the STORAGES setting from base.py (CompressedManifestStaticFilesStorage)
# But we need to relax strictness because of a missing Jcrop.gif in Wagtail 7.3a0
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "demo.settings.production.NonStrictCompressedManifestStaticFilesStorage",
    },
}

# Force Django to use the static() template tag correctly with manifest storage
# This ensures versioned_static resolves to hashed filenames
WAGTAILADMIN_STATIC_FILE_VERSION_STRINGS = False

# WhiteNoise configuration for better static file serving
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True
WHITENOISE_MANIFEST_STRICT = False

# Add static files debugging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Production settings loaded with manifest storage")

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
