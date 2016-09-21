from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from apps.stats import views as stats_views
from apps.users import views as user_views

from django.contrib.sitemaps.views import sitemap

from .sitemap import SITEMAPS

from rest_framework import routers
from rest_framework.authtoken import views as rest_view
from apps.stats import api as stats_api

router = routers.DefaultRouter()

router.register(r'fixtures', stats_api.FixtureViewSet)
router.register(r'recent_results', stats_api.RecentResultViewSet)
router.register(r'league_table', stats_api.LeagueTableViewSet, base_name='league_table')
router.register(r'top_scorers', stats_api.TopScorerViewSet, base_name='top_scorers')
router.register(r'injuries', stats_api.InjuryViewSet)


urlpatterns = patterns('',
                       url(r'^$', 'apps.core.views.home', name='home'),
                       # url(r'^$', 'apps.users.views.login_register', name='login_register'),
                       url(r'^(?P<devil_no>[0-9]+)/$', 'apps.users.views.devil_no_handler', name='devil_no'),
                       url(r'^m/(?P<slug>[a-zA-Z0-9_.-/+/@/-]+)/$', user_views.MemberProfileView.as_view(),
                           name='view_member_profile'),

                       url(r'^froala_editor/', include('froala_editor.urls')),

                       (r'^admin/settings/', include('dbsettings.urls')),
                       url(r'admin/clear-cache/', 'apps.core.views.clear_cache', name='clear_cache'),
                       (r'^admin/', include('smuggler.urls')),  # before admin url patterns!
                       url(r'^admin/', include(admin.site.urls)),
                       (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, 'logout'),
                       (r'^accounts/', include('allauth.urls')),
                       url(r'^membership/$', 'apps.users.views.membership_form', name='membership_form'),
                       url(r'^renew/$', 'apps.users.views.renew', name='renew'),
                       url(r'^membership/payment/$', 'apps.users.views.membership_payment', name='membership_payment'),
                       url(r'^membership/payment/esewa/success/$', 'apps.users.views.esewa_success',
                           name='membership_payment_esewa_success'),
                       url(r'^membership/payment/esewa/failure/$', 'apps.users.views.esewa_failure',
                           name='membership_payment_esewa_failure'),
                       url(r'^membership/thankyou/$', 'apps.users.views.membership_thankyou',
                           name='membership_thankyou'),

                       url(r'^members/$', user_views.PublicMembershipListView.as_view(), name='list_members'),
                       (r'^dashboard/', include('apps.dashboard.urls')),
                       (r'^event/', include('apps.events.urls')),
                       (r'^post/', include('apps.post.urls')),
                       (r'^timeline/', include('apps.timeline.urls')),

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
                       url(r'^epl-table/$', stats_views.epl_table, name='epl_table'),
                       url(r'^matchweek/$', stats_views.matchweek, name='matchweek'),
                       url(r'^fixtures/$', stats_views.fixtures, name='fixtures'),
                       url(r'^results/$', stats_views.fixtures, name='results'),
                       url(r'^top-scorers/$', stats_views.scorers, name='scorers'),
                       url(r'^injuries/$', stats_views.injuries, name='injuries'),
                       url(r'^sitemap\.xml$', sitemap, {'sitemaps': SITEMAPS},
                           name='django.contrib.sitemaps.views.sitemap'),
                       url(r'^partner/(?P<slug>[a-zA-Z0-9_.-]+)/$', 'apps.partner.views.view_partner',
                           name='view_partner'),
                       url(r'^team/$', 'apps.team.views.football_team', name='football_team'),

                       url(r'^match/(?P<date>[\d{4}\-\d{2}\-\d{2}]+)/(?P<extra>[a-zA-Z0-9_.-]*)/?$',
                           stats_views.FixtureDetail.as_view(),
                           name='fixture_detail'),
                       url(r'^gallery/', include('apps.gallery.urls')),

                       (r'^webhook/', include('apps.webhook.urls')),

                       (r'', include('apps.page.urls')),

                        #Rest API end points
                       url(r'api/v1/', include(router.urls)),
                       url(r'^obtain_auth_token/', rest_view.obtain_auth_token),
                       )

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT, 'show_indexes': True})
                            )
elif getattr(settings, 'FORCE_SERVE_STATIC', False):
    from django.conf.urls.static import static

    settings.DEBUG = True
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    settings.DEBUG = False

handler400 = 'apps.core.views.bad_request'
handler403 = 'apps.core.views.permission_denied'
handler404 = 'apps.core.views.page_not_found'
handler500 = 'apps.core.views.server_error'
