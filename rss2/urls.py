"""rss2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from __future__ import absolute_import, unicode_literals, division
import os
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from filebrowser.sites import site
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.static import serve
import django.contrib.auth.views

admin.autodiscover()
admin.site.site_header = 'Reiseservice Schwerin GmbH - Seitenverwaltung'
admin.site.site_title = 'Reiseservice Schwerin GmbH - Seitenverwaltung'

js_info_dict = {
    'packages': ('django.conf',),
}

urlpatterns = [
    url(r'^$', include('home.urls')),
    #url(r'^', include('home.urls')),
    url(r'^reisen/', include('reisen.urls')),
    url(r'^home/', include('home.urls')),
    #url(r'^locking/', include('locking.urls')),
    url(r'^filer/', include('filer.urls')),
    url(r'^inplaceeditform/', include('inplaceeditform.urls')),
    url(r'^jsi18n$', 'django.views.i18n.javascript_catalog', js_info_dict),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^admin/ajax/', include('locking.urls')),
    url(r'^accounts/login/$', django.contrib.auth.views.login),
    url(r'^accounts/logout/$', django.contrib.auth.views.logout, {'next_page': '/'}),
]

# --- DIESER TEIL IST NEU UND WICHTIG FÜR DOCKER ---
if settings.DEBUG:
    # 1. Standard Statics
    urlpatterns += staticfiles_urlpatterns()
    
    # 2. Media Files (Reisebilder) - Hier war der NameError
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # 3. Die Umleitung für die verirrten Muse-Pfade (/home/css/...)
    urlpatterns += [
        # Diese Zeile ist jetzt entscheidend:
        url(r'^home/scripts/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'static/scripts')}),
        
        # Die anderen können bleiben:
        url(r'^home/css/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'static/css')}),
        url(r'^home/images/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'static/images')}),
    ]
