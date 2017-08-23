from django.conf.urls import include, url
#from filebrowser.sites import site
import nested_admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^winter2016_17/$', views.winter2016_17, name='winter2016_17'),
    url(r'^winter2017_18/$', views.winter2017_18, name='winter2017_18'),
    url(r'^winter1617/$', views.winter1617, name='winter1617'),
    url(r'^winter1718/$', views.winter1718, name='winter1718'),
    url(r'^sommer17/$', views.sommer17, name='sommer17'),
    url(r'^tagesfahrten/$', views.tagesfahrten, name='tagesfahrten'),
    url(r'^winter2016_17_export/$', views.winter2016_17_export, name='winter2016_17_export'),
    url(r'^reiseterminuebersicht/$', views.reiseterminuebersicht, name='reiseterminuebersicht'),
    url(r'^reiseuebersichtwinter/$', views.reiseuebersichtwinter, name='reiseuebersichtwinter'),
    url(r'^reisezieluebersicht/$', views.reisezieluebersicht, name='reisezieluebersicht'),
    url(r'^reise_detail_export/(?P<pk>[-\w]+)/$', views.reise_detail_export, name='reise_detail_export'),
    url(r'^reise/(?P<pk>[\w]+)/$', views.reise_detail, name='reise_detail'),
    url(r'^reise/(?P<slug>[-_\w]+)/', views.reise_detail, name='reise_detail'),
    url(r'^reise/(?P<slug>[-_\w]+),(?P<pk>[\w]+)/', views.reise_detail, name='reise_detail'),
#    url(r'^reise/winter1617/(?P<pk>[\w]+)/$', views.reise_detail, name='reise_detail_web_alt'),
#    url(r'^reise/winter1617(?P<slug>[-_\w]+)/', views.reise_detail, name='reise_detail_web_alt'),
    #url(r'^admin/filebrowser/', include(site.urls)),
    #url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^nested_admin/', include('nested_admin.urls')),
]
