"""
WSGI config for rss2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rss2.settings.production")
os.environ['DJANGO_SETTINGS_MODULE'] = 'rss2.settings.production'

application = get_wsgi_application()
