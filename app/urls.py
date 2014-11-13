from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^$', 'core.views.home', name='home'),

                       url(r'^admin/', include(admin.site.urls)),
                       (r'^accounts/', include('allauth.urls')),
                       url(r'^register/$', 'users.views.membership_form', name='register'),
)
