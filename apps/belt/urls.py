from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^reg$', views.reg),
    url(r'^wish$', views.wish),
    url(r'^stats$', views.stats),
    url(r'^wish/(?P<id>\d+)$', views.wish),
    url(r'^form/$', views.form),
    url(r'^form/(?P<id>\d+)$', views.form),
    url(r'^granted/(?P<id>\d+)$', views.granted),
    url(r'^like/(?P<id>\d+)$', views.like),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
]
