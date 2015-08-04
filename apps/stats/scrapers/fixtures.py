import urllib
import json

class FixturesScraper():
    @classmethod
    def start(cls):
        from django.conf import settings

        api_key = settings.FOOTBALL_API_KEY
        # TODO make year dynamic
        url = 'http://football-api.com/api/?Action=fixtures&APIKey=' + api_key + '&comp_id=1204&from_date=01.08.2015&to_date=31.05.2016'
        print 'Retrieving from API'
        f = urllib.urlopen(url)
        data = json.loads(f.read())
        # from django.core.cache import cache
        # cache.set('fixtures', data, timeout=None)
        # data = cache.get('fixtures')
        # if not data['ERROR'] == 'OK':
        #     print 'Error: ' + data['ERROR']
        import ipdb

        ipdb.set_trace()

        # for match in data['matches']:


