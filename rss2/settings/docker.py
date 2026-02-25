# rss2/settings/docker.py
from .production import *

# Überschreibe die Datenbank-Verbindung für den Docker-Container
DATABASES['default']['NAME'] = 'rss2'
DATABASES['default']['USER'] = 'django'
DATABASES['default']['PASSWORD'] = 'MMu9U30iL!'
DATABASES['default']['HOST'] = 'db'  # Verweist auf den Service in docker-compose.yml

# Korrektur der Pfade für die lokale Umgebung
import os
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Prüfe, ob BASE_DIR wirklich dort landet, wo 'manage.py' liegt.
# Falls dein Projekt in /app liegt, sollte BASE_DIR '/app' sein.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Media-Dateien lokal im Projektordner speichern statt im festen CentOS-Pfad
# 3. Pfade für statische Dateien korrigieren
# In Docker laufen wir auf Port 8000 ohne das "/rss2" Präfix des Apache
FORCE_SCRIPT_NAME = None
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
FILEBROWSER_VERSIONS_BASEDIR = '_versionen/'

# 5. Debug-Modus für lokale Entwicklung einschalten
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True

# 6. Erlaube Docker-Zugriff
ALLOWED_HOSTS = ['*']

# 7. Absoluter Pfad Check für Custom Tags
# Falls Django die Tags immer noch nicht findet, erzwingen wir den Pfad
import sys
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Sagt Django, wo es zusätzlich nach statischen Dateien suchen soll
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]