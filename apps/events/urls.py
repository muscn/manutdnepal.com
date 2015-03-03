from django.conf.urls import patterns, url
from . import views



urlpatterns = patterns('',
                       url(r'^$', views.EventsList.as_view(), name='list_events'),
                       url(r'^(?P<slug>[a-zA-Z0-9_.-]+)/$', views.EventDetail.as_view(), name='view_event'),

)
