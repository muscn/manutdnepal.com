from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.PostList.as_view(), name='list_posts'),
    url(r'^(?P<slug>[a-zA-Z0-9_.-]+)/$', views.PostDetail.as_view(), name='view_post'),
]
