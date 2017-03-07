from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.aktuelles, name='aktuelles'),
    url(r'^gibReisen/$', views.gibReisen, name='gibReisen'),
    url(r'^ajax', views.ajax, name='ajax'),
    url(r'^neustart', views.neustart, name='neustart'),
    url(r'^start', views.start, name='start'),
    url(r'^reisen', views.reisen, name='reisen'),
    url(r'^tagesfahrten', views.tagesfahrten, name='tagesfahrten'),
    url(r'^musicals', views.musicals, name='musicals'),
    url(r'^reiseberatung', views.reiseberatung, name='reiseberatung'),
    url(r'^service', views.service, name='service'),
    url(r'^zusatzangebote', views.zusatzangebote, name='zusatzangebote'),
    url(r'^kontakt', views.kontakt, name='kontakt'),
    url(r'^aktuell/(?P<pk>[0-9]+)/$', views.aktuell_detail, name='aktuell_detail'),
    url(r'^new/$', views.aktuell_neu, name='aktuell_neu'),
    url(r'^aktuell/(?P<pk>[0-9]+)/edit/$', views.aktuell_edit, name='aktuell_edit'),
    url(r'^drafts/$', views.aktuell_draft_list, name='aktuell_draft_list'),
    url(r'^aktuell/(?P<pk>[0-9]+)/publish/$', views.aktuell_publish, name='aktuell_publish'),
    url(r'^aktuell/(?P<pk>[0-9]+)/remove/$', views.aktuell_remove, name='aktuell_remove'),
]
