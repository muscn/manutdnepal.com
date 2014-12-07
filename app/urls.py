from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^$', 'core.views.home', name='home'),
                       url(r'^admin/', include(admin.site.urls)),
                       (r'^accounts/', include('allauth.urls')),
                       url(r'^membership/$', 'users.views.membership_form', name='membership_form'),
                       url(r'^membership/payment$', 'users.views.membership_payment', name='membership_payment'),
                       url(r'^membership/thankyou$', 'users.views.membership_thankyou', name='membership_thankyou'),

)
