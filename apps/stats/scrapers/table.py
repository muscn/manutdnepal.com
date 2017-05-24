import datetime

import pytz
from django.core.cache import cache
from django.conf import settings

from apps.stats.models import Fixture
from .base import Scraper


class TableScraper(Scraper):
    base_url = 'http://www.livescores.com'

    @classmethod
    def scrape(cls):
        root = cls.get_root_tree()
        tz = pytz.timezone(settings.TIME_ZONE)
        if root is not None:
            rows = root.cssselect('div.ltable div.row-gray:not(div.title.row-gray)')
            cls.data['teams'] = []
            for row in rows:
                data = {}
                cols = row.cssselect('div')
                # cols[0] is self
                try:
                    if len(cols[1].cssselect('span.live img')):
                        data['live'] = True
                    else:
                        data['live'] = False
                    data['position'] = cols[1].cssselect('span')[1].text_content()
                    data['name'] = cols[2].text_content()
                    data['p'] = cols[3].text_content()
                    data['w'] = cols[4].text_content()
                    data['d'] = cols[5].text_content()
                    data['l'] = cols[6].text_content()
                    data['f'] = cols[7].text_content()
                    data['a'] = cols[8].text_content()
                    data['gd'] = cols[9].text_content()
                    data['pts'] = cols[10].text_content()
                    cls.data['teams'].append(data)
                except IndexError:
                    pass

            # Also fetch all matches this week

            matches = root.cssselect('div[data-type="evt"]')
            cls.data['matches'] = {}
            for match in matches:
                data = {'eid': match.get('data-eid')}
                minute = match.cssselect('div.min')[0].text_content().strip()
                data['minute'] = minute
                if "'" in minute:
                    data['live'] = True
                else:
                    data['live'] = False
                dt = tz.localize(datetime.datetime.strptime(match.get('data-esd'), '%Y%m%d%H%M%S'))
                data['kickoff'] = dt
                date = dt.date()
                data['home_team'] = match.cssselect('div.ply.tright.name')[0].text_content().strip()
                data['away_team'] = match.cssselect('div.ply.name:not(.tright)')[0].text_content().strip()
                data['score'] = match.cssselect('div.sco')[0].text_content().strip()
                if date not in cls.data['matches']:
                    cls.data['matches'][date] = []
                cls.data['matches'][date].append(data)
                if data['home_team'] in settings.ALIASES or data['away_team'] in settings.ALIASES:
                    links = match.cssselect('div.sco')[0].cssselect('a')
                    if len(links):
                        url = cls.base_url + links[0].get('href')
                        m_data = cls.get_m_data(url)
                        if m_data:
                            m_data['minute'] = data['minute']
                            try:
                                try:
                                    fixture = Fixture.objects.get(datetime=dt)
                                except Fixture.MultipleObjectsReturned:
                                    fixture = Fixture.objects.filter(datetime=dt).first()
                                    fixtures_to_delete = Fixture.objects.filter(datetime=dt)[1:].values_list("id", flat=True)
                                    Fixture.objects.filter(pk__in=list(fixtures_to_delete)).delete()
                                if not fixture.has_complete_data():
                                    fixture.process_data(data, m_data)
                                    if data['minute'] == 'FT':
                                        fixture.send_updates()
                            except Fixture.DoesNotExist:
                                print 'Fixture does not exist.'

    @classmethod
    def get_m_data(cls, url):
        # Has OG by opponent
        # url = 'http://www.livescore.com/soccer/england/premier-league/manchester-united-vs-crystal-palace/1-1989005/'
        # Has OG by Utd
        # url = 'http://www.livescore.com/soccer/england/premier-league/sunderland-vs-manchester-united/1-1988968/'
        # Penalty scored at away
        # url = 'http://www.livescore.com/soccer/england/premier-league/newcastle-united-vs-manchester-united/1-1988916/'
        root = cls.get_root_tree(url)
        if root is not None:
            data = {'events': []}
            grays = root.cssselect('div.row-gray')
            for gray in grays:
                # HT Score
                # IndexError for match which have not been played.
                try:
                    if len(gray.cssselect('div.ply.tright')) and gray.cssselect('div.ply.tright')[
                        0].text_content().strip() == 'half-time:':
                        data['ht_score'] = gray.cssselect('div.sco')[0].text_content().replace('(', '').replace(')',
                                                                                                                '').replace(
                            ' ', '')
                        continue
                    # All but HT Score are events
                    event = {}
                    # Goal
                    if len(gray.cssselect('div.sco')) and gray.cssselect('div.sco')[0].text_content().strip():
                        event['type'] = 'goal'
                        score = gray.cssselect('div.sco')[0].text_content().strip()
                        event['text'] = score
                        m = gray.cssselect('.min')[0].text_content().strip().replace("'", "")
                        event['m'] = m
                        home_scorer = \
                            gray.cssselect('div.ply.tright')[0].cssselect('div:not(.ply)')[0].cssselect('.name')[
                                0].text_content().strip()
                        og = False
                        pen = False
                        for ply in gray.cssselect('div.ply'):
                            # og
                            if len(ply.cssselect('span.ml4')) and ply.cssselect('span.ml4')[0].text_content().strip() == '(o.g.)':
                                og = True
                            if len(ply.cssselect('span.mr4')) and ply.cssselect('span.mr4')[0].text_content().strip() == '(o.g.)':
                                og = True
                            # pen
                            if len(ply.cssselect('span.ml4')) and ply.cssselect('span.ml4')[0].text_content().strip() == '(pen.)':
                                pen = True
                            if len(ply.cssselect('span.mr4')) and ply.cssselect('span.mr4')[0].text_content().strip() == '(pen.)':
                                pen = True
                            # Assist
                            if len(ply.cssselect('.assist.name')):
                                event['assist_by'] = ply.cssselect('.assist.name')[0].text_content().replace('(assist)',
                                                                                                             '').strip()
                        if home_scorer:
                            if og:
                                event['team'] = 'away'
                            else:
                                event['team'] = 'home'
                            event['scorer'] = home_scorer
                        else:
                            if og:
                                event['team'] = 'home'
                            else:
                                event['team'] = 'away'
                            event['scorer'] = \
                                gray.cssselect('div.ply:not(.tright)')[0].cssselect('div:not(.ply)')[0].cssselect(
                                    '.name')[
                                    0].text_content().strip()
                        if og:
                            event['og'] = True
                        if pen:
                            event['pen'] = True

                        data['events'].append(event)
                        continue
                except IndexError:
                    pass
            return data


class EPLScrape(TableScraper):
    @property
    def url(self):
        return self.base_url + '/soccer/england/premier-league/'

    @classmethod
    def save(cls):
        cache.set('epl_standings', cls.data, timeout=None)


class LeagueCupScrape(TableScraper):
    @property
    def url(self):
        return self.base_url + '/soccer/england/carling-cup/'

    @classmethod
    def save(cls):
        cache.set('league_cup_standings', cls.data, timeout=None)


class FACupScrape(TableScraper):
    @property
    def url(self):
        return self.base_url + '/soccer/england/fa-cup/'

    @classmethod
    def save(cls):
        cache.set('fa_cup_standings', cls.data, timeout=None)


class EuropaLeagueScrape(TableScraper):
    @property
    def url(self):
        return self.base_url + '/soccer/europa-league/'

    @classmethod
    def save(cls):
        cache.set('europa_league_standings', cls.data, timeout=None)
