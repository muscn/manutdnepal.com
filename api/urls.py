from django.conf.urls import url
from api import views

urlpatterns = (
    url(r'^/', views.index),
    url(r'^users/$', views.users),
    url(r'^users/(?P<id>[0-9]+)/$', views.users),
    url(r'^login/$', views.user_login),
)
