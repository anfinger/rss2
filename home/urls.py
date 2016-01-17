from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.aktuelles, name='aktuelles'),
    url(r'^aktuell/(?P<pk>[0-9]+)/$', views.aktuell_detail, name='aktuell_detail'),
    url(r'^new/$', views.aktuell_neu, name='aktuell_neu'),
    url(r'^aktuell/(?P<pk>[0-9]+)/edit/$', views.aktuell_edit, name='aktuell_edit'),
    url(r'^drafts/$', views.aktuell_draft_list, name='aktuell_draft_list'),
    url(r'^aktuell/(?P<pk>[0-9]+)/publish/$', views.aktuell_publish, name='aktuell_publish'),
    url(r'^aktuell/(?P<pk>[0-9]+)/remove/$', views.aktuell_remove, name='aktuell_remove'),
]
