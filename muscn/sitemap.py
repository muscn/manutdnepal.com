import datetime

from django.contrib.sitemaps import Sitemap
from apps.events.models import Event
from apps.page.models import Page
from apps.partner.models import Partner
from apps.post.models import Post
from apps.stats.models import SeasonData, Player


class EventSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Event.objects.filter(enabled=True)


class PageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Page.objects.filter(status='Published')

    def lastmod(self, obj):
        return obj.updated_at


class PartnerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Partner.objects.filter(active=True)


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Post.objects.filter(status='Published')

    def lastmod(self, obj):
        return obj.created_at


class SeasonSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return SeasonData.objects.all()


class PlayerSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Player.objects.all()


SITEMAPS = {
    'events': EventSitemap,
    'pages': PageSitemap,
    'partners': PartnerSitemap,
    'posts': PostSitemap,
    'seasons': SeasonSitemap,
    'players': PlayerSitemap,
}