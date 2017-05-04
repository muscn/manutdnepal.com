from django.conf.urls import url

from . import views

urlpatterns = [
       url(r'^(?P<slug>[a-zA-Z0-9_.-]+)/$', views.view_page, name='view_page'),
]
