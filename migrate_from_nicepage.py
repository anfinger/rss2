# Vorbereitung .. rss3_web ist der docker web container
# docker exec -it rss3_web pip install beautifulsoup4 requests
# docker exec -it rss3_web python migrate_from_nicepage.py
# docker exec -it rss3_web python manage.py collectstatic --noinput

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# --- KONFIGURATION ---
URL = "https://reiseserviceschwerin.nicepage.io/"
BASE_DIR = "home/templates/home/partials"
FULL_DIR = "home/templates/home"
STATIC_DIR = "home/static/home"
# ---------------------

def setup_folders():
    for d in [BASE_DIR, FULL_DIR, f"{STATIC_DIR}/css", f"{STATIC_DIR}/js", f"{STATIC_DIR}/images"]:
        os.makedirs(d, exist_ok=True)

def download_asset(url, folder):
    if not url or url.startswith('data:') or url.startswith('#'): return url
    # Verhindere, dass externe Google Fonts etc. lokal gesucht werden
    if "fonts.googleapis" in url: return url
    
    filename = os.path.basename(urlparse(url).path)
    if not filename: return url
    
    filepath = os.path.join(STATIC_DIR, folder, filename)
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(resp.content)
            print(f"    📥 Download erfolgreich: {filename}")
            return f"{{% static 'home/{folder}/{filename}' %}}"
    except Exception as e:
        print(f"    ❌ Fehler bei {filename}: {e}")
    return url

def migrate():
    setup_folders()
    print(f"🚀 Starte Migration von {URL}...")
    response = requests.get(URL)
    response.encoding = 'utf-8' 
    soup = BeautifulSoup(response.text, 'html.parser')

    # 1. CSS Dateien herunterladen & Pfade anpassen
    print("🎨 Verarbeite Stylesheets...")
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href')
        if href:
            full_url = urljoin(URL, href)
            link['href'] = download_asset(full_url, 'css')

    # 2. JavaScript Dateien herunterladen & Pfade anpassen
    print("⚙️ Verarbeite Scripts...")
    for script in soup.find_all('script', src=True):
        src = script.get('src')
        if src:
            full_url = urljoin(URL, src)
            script['src'] = download_asset(full_url, 'js')

    # 3. Bilder herunterladen & Pfade anpassen
    print("🖼️ Verarbeite Bilder...")
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            full_url = urljoin(URL, src)
            img['src'] = download_asset(full_url, 'images')

    # 4. Partials extrahieren
    print("✂️ Erstelle Partials...")
    tags_to_extract = soup.find_all(['header', 'footer', 'section'])
    for i, element in enumerate(tags_to_extract):
        el_id = element.get('id', f"part-{element.name}-{i}")
        file_path = os.path.join(BASE_DIR, f"__{el_id}.html")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("{% load static %}\n")
            f.write(element.prettify())
        print(f"  ✅ Partial: __{el_id}.html")

    # 5. Gesamtdatei für base.html Vorlage
    full_html_path = os.path.join(FULL_DIR, "nicepage_full_preview.html")
    with open(full_html_path, 'w', encoding='utf-8') as f:
        f.write("{% load static %}\n" + soup.prettify())
    
    print(f"\n✨ Fertig! CSS, JS und Bilder sollten jetzt aktuell sein.")

if __name__ == "__main__":
    migrate()