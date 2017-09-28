from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import logout
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from apps.team import views as team_views
from apps.stats import views as stats_views
from apps.partner import views as partner_views

from .sitemap import SITEMAPS

from rest_framework import routers
from apps.stats import api as stats_api
from apps.events import api as events_api
from apps.post import api as post_api
from apps.page import api as page_api
from apps.push_notification import api as push_notification_api
from apps.users import api as user_api
from apps.partner import api as partner_api

from apps.core import views as core_views
from apps.users import views as user_views

router = routers.DefaultRouter()

router.register(r'fixtures', stats_api.FixtureViewSet)
router.register(r'fixture_detail', stats_api.FixtureDetailViewSet)
router.register(r'recent_results', stats_api.RecentResultViewSet)
router.register(r'league_table', stats_api.LeagueTableViewSet, base_name='league_table')
router.register(r'top_scorers', stats_api.TopScorerViewSet, base_name='top_scorers')
router.register(r'injuries', stats_api.InjuryViewSet)
router.register(r'squads', stats_api.SquadViewSet)
router.register(r'partners', partner_api.PartnerViewSet)
router.register(r'past_seasons', stats_api.PastSeasonViewSet)

router.register(r'user_device', push_notification_api.UserDeviceViewSet)

router.register(r'events', events_api.EventViewSet)

router.register(r'posts', post_api.PostViewSet)

router.register(r'pages', page_api.PageViewSet)

router.register(r'users', user_api.UserViewSet)

urlpatterns = [

    url(r'^$', core_views.home, name='home'),

    # url(r'^$', 'apps.users.views.login_register', name='login_register'),
    url(r'^(?P<devil_no>[0-9]+)/$', user_views.devil_no_handler, name='devil_no'),
    url(r'^m/(?P<slug>.*)/$', user_views.MemberProfileView.as_view(), name='view_member_profile'),
    url(r'^froala_editor/', include('froala_editor.urls')),
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'muadmin/clear-cache/', core_views.clear_cache, name='clear_cache'),

    url(r'^muadmin/', include(admin.site.urls)),
    url(r'^logout/$', logout, {'next_page': '/'}, 'logout'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^membership/$', user_views.membership_form, name='membership_form'),
    # url(r'^renew/$', user_views.renew, name='renew'),
    url(r'^membership/esewa/$', user_views.esewa_form, name='esewa_form'),
    # url(r'^membership/payment/$', user_views.membership_payment, name='membership_payment'),
    url(r'^membership/payment/esewa/success/$', user_views.esewa_success, name='membership_payment_esewa_success'),
    url(r'^membership/payment/esewa/failure/$', user_views.esewa_failure, name='membership_payment_esewa_failure'),
    # url(r'^membership/thankyou/$', user_views.membership_thankyou, name='membership_thankyou'),

    url(r'^members/$', user_views.PublicMembershipListView.as_view(), name='list_members'),
    url(r'^dashboard/', include('apps.dashboard.urls')),
    url(r'^event/', include('apps.events.urls')),
    url(r'^post/', include('apps.post.urls')),
    url(r'^timeline/', include('apps.timeline.urls')),
    url(r'^contact-us/', include('apps.contact.urls')),

    url(r'^seasons/$', stats_views.SeasonDataListView.as_view(), name='list_seasons'),
    url(r'^season/(?P<year>[\d]{4})-(?P<year1>[\d]{2})/(?P<competition>[a-zA-Z0-9_.-]+)/$',
        stats_views.SeasonCompetitionView.as_view(), name='view_season_competition'),
    url(r'^season/(?P<year>[\d]{4})-(?P<year1>[\d]{2})/$', stats_views.SeasonDataDetailView.as_view(), name='view_seasondata'),
    url(r'^seasons/$', stats_views.SeasonDataListView.as_view(), name='list_seasons'),
    url(r'^squad/$', stats_views.SquadListView.as_view(), name='list_squad'),
    url(r'^player/(?P<slug>[a-zA-Z0-9_.-]+)/$', stats_views.PlayerDetailView.as_view(), name='view_player'),
    url(r'^epl-table/$', stats_views.epl_table, name='epl_table'),
    url(r'^matchweek/$', stats_views.matchweek, name='matchweek'),
    url(r'^fixtures/$', stats_views.fixtures, name='fixtures'),
    url(r'^results/$', stats_views.fixtures, name='results'),

    url(r'^league/(?P<slug>[a-zA-Z0-9_.-]+)/$', stats_views.CompetitionDetail.as_view(), name='competition-detail'),

    url(r'^all-results/$', stats_views.all_results, name='all-results'),
    url(r'^top-scorers/$', stats_views.scorers, name='scorers'),
    url(r'^injuries/$', stats_views.injuries, name='injuries'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': SITEMAPS}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^partner/(?P<slug>[a-zA-Z0-9_.-]+)/$', partner_views.view_partner, name='view_partner'),
    url(r'^team/$', team_views.football_team, name='football_team'),

    url(r'^match/(?P<date>[\d{4}\-\d{2}\-\d{2}]+)/(?P<extra>[a-zA-Z0-9_.-]*)/?$', stats_views.FixtureDetail.as_view(),
        name='fixture_detail'),
    url(r'^gallery/', include('apps.gallery.urls')),

    # (r'^webhook/', include('apps.webhook.urls')),

    url(r'', include('apps.page.urls')),

    url(r'^api/v1/obtain_auth_token/', user_api.CustomObtainAuth.as_view()),

    # Rest API end points
    url(r'api/v1/', include(router.urls)),

    url(r'fcm/', include('fcm.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
