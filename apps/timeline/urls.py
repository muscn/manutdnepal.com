from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       # url(r'^$', views.PostList.as_view(), name='list_posts'),
                       url(r'^(?P<slug>[a-zA-Z0-9_.-]+)/$', views.TimelineDetail.as_view(), name='view_timeline'),
                       )
