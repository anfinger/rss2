from django.urls import include, re_path, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views # Wichtig für Login/Logout
from django.views.i18n import JavaScriptCatalog
from filebrowser.sites import site


admin.autodiscover()
admin.site.site_header = 'Reiseservice Schwerin GmbH - Seitenverwaltung'
admin.site.site_title = 'Reiseservice Schwerin GmbH - Seitenverwaltung'

urlpatterns = [
    path('reisen/', include('reisen.urls')),

    # Korrekt: Kein $ bei include(), damit Unterpfade wie /index/ funktionieren
    path('', include('home.urls')), 
    
    path('home/', include('home.urls')),
    path('filer/', include('filer.urls')),
    
    # Rest bleibt gleich...
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('admin/filebrowser/', site.urls),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    
    # Login / Logout
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

# Am Ende der Datei anfügen:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)