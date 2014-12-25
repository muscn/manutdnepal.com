from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # url(r'^$', 'core.views.home', name='home'),
                       url(r'^$', 'users.views.login_register', name='login_register'),
                       (r'^admin/settings/', include('dbsettings.urls')),
                       url(r'admin/clear-cache/', 'core.views.clear_cache', name='clear_cache'),
                       url(r'^admin/', include(admin.site.urls)),
                       (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, 'logout'),
                       (r'^accounts/', include('allauth.urls')),
                       url(r'^membership/$', 'users.views.membership_form', name='membership_form'),
                       url(r'^membership/payment/$', 'users.views.membership_payment', name='membership_payment'),
                       url(r'^membership/thankyou/$', 'users.views.membership_thankyou', name='membership_thankyou'),
                       url(r'^home/$', 'core.views.home', name='home'),

                       (r'', include('page.urls')),
)
