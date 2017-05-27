from django.conf.urls import url

from . import views
# from rest_framework.urlpatterns import format_suffix_patterns
from . import api

web_urls = [
url(r'^admin/upload/(?P<pk>\d+)/$', views.multi_upload, name='multi-upload'),
    url(r'^admin/delete/(?P<pk>\d+)/$', views.upload_delete, name='image-delete'),
    url(r'^$', views.album_list, name='album-list'),
    url(r'^(?P<slug>[\w-]+)/', views.AlbumDetail.as_view(), name='album-images'),
]

api_urls = [
    #     url(r'^api/images/$', api.ImageListAPI.as_view()),
    #     url(r'^api/albums/$', api.AlbumListAPI.as_view()),
    #     url(r'^api/albums/(?P<pk>\d+)/$', api.AlbumDetailAPI.as_view()),
]

# api_urls = format_suffix_patterns(api_urls)

urlpatterns = web_urls + api_urls
