from django.conf.urls import include, url
from filebrowser.sites import site
import nested_admin

from . import views, bastel_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^bastel/$', bastel_views.index, name='indexpopindex'),
    url(r'^bastel/reise/(?P<pk>[\w]+)/$', bastel_views.reise_detail, name='detailpopail'),
    url(r'^reise/(?P<pk>[\w]+)/$', views.reise_detail, name='reise_detail'),
    #url(r'^reise/(?P<slug>[-_\w]+)/', views.reise_detail, name='reise_detail'),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^nested_admin/', include('nested_admin.urls')),
]
