from django.core.cache import cache

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
        

    @classmethod
    def save(cls):
        cache.set('epl_standings', cls.data, timeout=None)
