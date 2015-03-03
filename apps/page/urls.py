from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^(?P<slug>[a-zA-Z0-9_.-]+)/$', views.view_page, name='view_page'),
)
