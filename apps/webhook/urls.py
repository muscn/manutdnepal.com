from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^log/(?P<request_type>[a-zA-Z0-9_.-]+)/$', views.logger, name='logger'),
]
