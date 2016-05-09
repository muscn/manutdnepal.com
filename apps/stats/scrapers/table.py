import datetime

from django.core.cache import cache
from django.conf import settings

from apps.stats.models import Fixture
from .base import Scraper


class TableScraper(Scraper):
    base_url = 'http://www.livescore.com'
    url = 'http://www.livescore.com/soccer/england/premier-league/'

    @classmethod
    def scrape(cls):

        root = cls.get_root_tree()
        rows = root.cssselect('div.ltable div.row-gray:not(div.title.row-gray)')
        cls.data['teams'] = []
        for row in rows:
            data = {}
            cols = row.cssselect('div')
            # cols[0] is self
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

        # Also fetch all matches this week

        matches = root.cssselect('div[data-type="evt"]')
        cls.data['matches'] = {}
        for match in matches:
            data = {}
            data['eid'] = match.get('data-eid')
            minute = match.cssselect('div.min')[0].text_content().strip()
            data['minute'] = minute
            if "'" in minute:
                data['live'] = True
            else:
                data['live'] = False
            dt = datetime.datetime.strptime(match.get('data-esd'), '%Y%m%d%H%M%S')
            # dt = dt.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone(settings.TIME_ZONE))
            data['kickoff'] = dt
            date = dt.date()
            data['home_team'] = match.cssselect('div.ply.tright.name')[0].text_content().strip()
            data['away_team'] = match.cssselect('div.ply.name:not(.tright)')[0].text_content().strip()
            data['score'] = match.cssselect('div.sco')[0].text_content().strip()
            if not date in cls.data['matches']:
                cls.data['matches'][date] = []
            cls.data['matches'][date].append(data)
            if data['home_team'] in settings.ALIASES or data['away_team'] in settings.ALIASES:
                links = match.cssselect('div.sco')[0].cssselect('a')
                if len(links):
                    url = cls.base_url + links[0].get('href')
                    m_data = cls.get_m_data(url)
                    try:
                        fixture = Fixture.objects.get(datetime=dt)
                        if not fixture.has_complete_data():
                            fixture.process_data(data, m_data)
                    except Fixture.DoesNotExist:
                        pass

    @classmethod
    def get_m_data(cls, url):
        # 3-2, double yellow = red card
        # url = 'http://www.livescore.com/soccer/england/premier-league/sunderland-vs-chelsea/1-1989077/'
        # Has OG by opponent
        # url = 'http://www.livescore.com/soccer/england/premier-league/manchester-united-vs-crystal-palace/1-1989005/'
        # Has OG by Utd
        # url = 'http://www.livescore.com/soccer/england/premier-league/sunderland-vs-manchester-united/1-1988968/'
        root = cls.get_root_tree(url)
        data = {'events': []}
        grays = root.cssselect('div.row-gray')
        for gray in grays:
            # HT Score
            if len(gray.cssselect('div.ply.tright')) and gray.cssselect('div.ply.tright')[
                0].text_content().strip() == 'half-time:':
                data['ht_score'] = gray.cssselect('div.sco')[0].text_content().replace('(', '').replace(')', '').replace(' ', '')
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
                home_scorer = gray.cssselect('div.ply.tright')[0].cssselect('div:not(.ply)')[0].cssselect('.name')[
                    0].text_content().strip()
                og = False
                for ply in gray.cssselect('div.ply'):
                    if len(ply.cssselect('span.ml4')) and ply.cssselect('span.ml4')[0].text_content().strip() == '(o.g.)':
                        og = True
                        break
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
                    event['scorer'] = gray.cssselect('div.ply:not(.tright)')[0].cssselect('div:not(.ply)')[0].cssselect('.name')[
                        0].text_content().strip()

                if og:
                    event['og'] = True
                data['events'].append(event)
                continue
        return data

    @classmethod
    def save(cls):
        cache.set('epl_standings', cls.data, timeout=None)
