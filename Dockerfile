# Wir nutzen das offizielle Python 3.12 Bild
FROM python:3.12-slim

# Verhindert, dass Python .pyc Dateien schreibt und sorgt für sofortige Logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# System-Abhängigkeiten für MySQL, Pillow (Bilder) und gettext
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libjpeg-dev \
    zlib1g-dev \
    gettext \
    git \
    libimage-exiftool-perl \
    && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis im Container
WORKDIR /app

# Requirements kopieren und installieren
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Den Rest des Codes kopieren
COPY . /app/

# Port 8000 für Django öffnen
EXPOSE 8000