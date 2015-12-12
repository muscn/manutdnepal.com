from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^log/(?P<request_type>[a-zA-Z0-9_.-]+)/$', views.logger, name='logger'),
)
