import datetime

import pytz

from django.core.cache import cache
from django.conf import settings

from .base import Scraper


class TableScraper(Scraper):
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

    @classmethod
    def save(cls):
        print cls.data['matches']
        cache.set('epl_standings', cls.data, timeout=None)
