from django.conf.urls import include, url
import nested_admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^nested_admin/', include('nested_admin.urls')),
]
