from datetime import datetime

from .base import Scraper
from apps.stats.models import Fixture
import pytz


class TVScraper(Scraper):
    channels = {'star-sports-4-india': 'Star Sports 4', 'star-sports-india':'Star Sports 1'}

    @classmethod
    def scrape(cls):
        json_data = cls.get_json_from_url('http://www.livesoccertv.com/m/api/teams/england/manchester-united/?iso_code=np')
        if 'fixtures' in json_data:
            for fixture in json_data['fixtures']:
                channels = fixture.get('channels')
                for channel in channels:
                    if channel.get('slug') in cls.channels:
                        cls.data[float(fixture.get('timestamp'))] = channel.get('name')
                        continue

    @classmethod
    def save(cls):
        for timest, channel in cls.data.iteritems():
            dt = datetime.utcfromtimestamp(timest).replace(tzinfo=pytz.UTC)
            fixture = Fixture.objects.get(datetime=dt)
            fixture.broadcast_on = channel
            fixture.save()
