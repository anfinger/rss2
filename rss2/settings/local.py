# settings/local.py

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rss2',
        'USER': 'django',
        'PASSWORD': 'MMu9U30iL',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

INSTALLED_APPS += (
    "debug_toolbar",
)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_PATCH_SETTINGS = False
