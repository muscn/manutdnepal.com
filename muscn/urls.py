from django.conf.urls import patterns, include, url
from django.contrib import admin

from apps.stats import views as stats_views


urlpatterns = patterns('',
                       # url(r'^$', 'core.views.home', name='home'),
                       url(r'^$', 'apps.users.views.login_register', name='login_register'),
                       (r'^admin/settings/', include('dbsettings.urls')),
                       url(r'admin/clear-cache/', 'apps.core.views.clear_cache', name='clear_cache'),
                       (r'^admin/', include('smuggler.urls')),  # before admin url patterns!
                       url(r'^admin/', include(admin.site.urls)),
                       (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, 'logout'),
                       (r'^accounts/', include('allauth.urls')),
                       url(r'^membership/$', 'apps.users.views.membership_form', name='membership_form'),
                       url(r'^membership/payment/$', 'apps.users.views.membership_payment', name='membership_payment'),
                       url(r'^membership/payment/esewa/success/$', 'apps.users.views.esewa_success',
                           name='membership_payment_esewa_success'),
                       url(r'^membership/payment/esewa/failure/$', 'apps.users.views.esewa_failure',
                           name='membership_payment_esewa_failure'),
                       url(r'^membership/thankyou/$', 'apps.users.views.membership_thankyou',
                           name='membership_thankyou'),
                       url(r'^home/$', 'apps.core.views.home', name='home'),

                       (r'dashboard/', include('apps.dashboard.urls')),

                       url(r'^seasons/$', stats_views.SeasonDataListView.as_view(), name='list_seasons'),
                       url(r'^season/(?P<year>[\d]{4})-(?P<year1>[\d]{2})/(?P<competition>[a-zA-Z0-9_.-]+)/$',
                           stats_views.SeasonCompetitionView.as_view(), name='view_season_competition'),
                       url(r'^season/(?P<year>[\d]{4})-(?P<year1>[\d]{2})/$',
                           stats_views.SeasonDataDetailView.as_view(),
                           name='view_seasondata'),
                       url(r'^seasons/$', stats_views.SeasonDataListView.as_view(), name='list_seasons'),
                       url(r'^squad/$', stats_views.SquadListView.as_view(), name='list_squad'),
                       url(r'^player/(?P<slug>[a-zA-Z0-9_.-]+)/$', stats_views.PlayerDetailView.as_view(),
                           name='view_player'),

                       (r'', include('apps.page.urls')),
)