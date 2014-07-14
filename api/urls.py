from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),

    url(r'^get_latest/$', views.get_latest, name='get_latest'),
)
