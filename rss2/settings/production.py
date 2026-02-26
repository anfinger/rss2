# settings/production.py

from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Wir holen uns die Werte aus der Umgebung, falls sie da sind, 
# ansonsten nutzen wir Standardwerte für die lokale Entwicklung
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'rss2'),
        'USER': os.environ.get('DB_USER', 'django'),
        'PASSWORD': os.environ.get('DB_PASS', 'MMu9U30iL!'),
        'HOST': os.environ.get('DB_HOST', 'db'), # In Docker ist 'db' die Adresse
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}