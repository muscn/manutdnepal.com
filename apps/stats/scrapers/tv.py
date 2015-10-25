from datetime import datetime

from .base import Scraper
from apps.stats.models import Fixture
import pytz


class TVScraper(Scraper):
    channels = {'star-sports-india': 'Star Sports 1',
                'star-sports-2-india': 'Star Sports 2',
                'star-sports-3-india': 'Star Sports 3',
                'star-sports-4-india': 'Star Sports 4',
                'star-sports-hd-1-india': 'Star Sports HD 1',
                'star-sports-hd-2-india': 'Star Sports HD 2',
                'sony-six-india': 'Sony Six',
                'sony-six-hd-india': 'Sony Six HD',
                'sony-kix-india': 'Sony Kix',
                'ten-sports': 'TEN Sports',
                'ten-action': 'Ten Action',
                }

    @classmethod
    def scrape(cls):
        json_data = cls.get_json_from_url(
            'http://www.livesoccertv.com/m/api/teams/england/manchester-united/?iso_code=np')
        if 'fixtures' in json_data:
            for fixture in json_data['fixtures']:
                channels = fixture.get('channels')
                for channel in channels:
                    if channel.get('slug') in cls.channels:
                        cls.data[float(fixture.get('timestamp'))] = cls.channels.get(channel.get('slug'))
                        continue

    @classmethod
    def save(cls):
        for timest, channel in cls.data.iteritems():
            dt = datetime.utcfromtimestamp(timest).replace(tzinfo=pytz.UTC)
            fixture = Fixture.objects.get(datetime=dt)
            fixture.broadcast_on = channel
            fixture.save()
