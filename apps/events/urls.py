from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.EventsList.as_view(), name='list_events'),
    url(r'^(?P<slug>[a-zA-Z0-9_.-]+)/$', views.EventDetail.as_view(), name='view_event'),

]
