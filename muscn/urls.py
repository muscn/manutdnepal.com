from django.conf.urls import patterns, include, url
from django.contrib import admin
from apps.stats import views as stats_views

urlpatterns = patterns('',
                       # url(r'^$', 'core.views.home', name='home'),
                       url(r'^$', 'apps.users.views.login_register', name='login_register'),
                       (r'^admin/settings/', include('dbsettings.urls')),
                       url(r'admin/clear-cache/', 'apps.core.views.clear_cache', name='clear_cache'),
                       url(r'^admin/', include(admin.site.urls)),
                       (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, 'logout'),
                       (r'^accounts/', include('allauth.urls')),
                       url(r'^membership/$', 'apps.users.views.membership_form', name='membership_form'),
                       url(r'^membership/payment/$', 'apps.users.views.membership_payment', name='membership_payment'),
                       url(r'^membership/thankyou/$', 'apps.users.views.membership_thankyou',
                           name='membership_thankyou'),
                       url(r'^home/$', 'apps.core.views.home', name='home'),

                       (r'dashboard/', include('apps.dashboard.urls')),

                       url(r'^seasons/$', stats_views.SeasonDataListView.as_view(), name='list_seasons'),

                       (r'', include('apps.page.urls')),
)
