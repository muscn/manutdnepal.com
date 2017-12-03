import datetime

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.events.models import Event
from apps.page.models import Page
from apps.partner.models import Partner
from apps.post.models import Post
from apps.stats.models import SeasonData, Player
from apps.users.models import User


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
        return Partner.objects.all()


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


class MembersSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return User.objects.all()


class DefaultNamedURLSitemap(Sitemap):
    """ Given a set of named URLs, returns sitemap items for each. """
    changefreq = 'weekly'

    def __init__(self, names):
        self.names = names
        self.priority = 0.1
        Sitemap.__init__(self)

    def items(self):
        return self.names

    @classmethod
    def location(cls, obj):
        return reverse(obj)


SITEMAPS = {
    'events': EventSitemap,
    'pages': PageSitemap,
    'partners': PartnerSitemap,
    'posts': PostSitemap,
    'seasons': SeasonSitemap,
    'players': PlayerSitemap,
    'members': MembersSitemap,
    'default_named_pages': DefaultNamedURLSitemap([
        'fixtures',
        'results',
        'epl_table',
        'scorers',
        'list_squad',
        'list_seasons',
        'membership_form',
        'list_members',
        'injuries',
        'football_team',
    ]),
}
