from ics import Calendar
from .base import Scraper
from apps.stats.models import Fixture, CompetitionYear, Competition, Team
from muscn.utils.football import get_current_season_start_year


class FixturesScraper(Scraper):
    # @classmethod
    # def start(cls):
    #     from django.conf import settings
    #
    #     api_key = settings.FOOTBALL_API_KEY
    #     # TODO make year dynamic
    #     url = 'http://football-api.com/api/?Action=fixtures&APIKey=' + api_key + '&comp_id=1204&from_date=01.08.2015&to_date=31.05.2016'
    #     print 'Retrieving from API'
    #     f = urllib.urlopen(url)
    #     data = json.loads(f.read())
    #     # from django.core.cache import cache
    #     # cache.set('fixtures', data, timeout=None)
    #     # data = cache.get('fixtures')
    #     # if not data['ERROR'] == 'OK':
    #     #     print 'Error: ' + data['ERROR']
    #     # for match in data['matches']:

    @classmethod
    def scrape(cls):
        url = 'http://calendar.manutd.com/Manchester_United.ics'
        year = str(get_current_season_start_year())
        # url = 'http://hackeragenda.urlab.be/events/events.ics'
        cal_content = cls.get_url_content(url)
        cal_content = cal_content.replace('RATE:', 'RDATE:')
        cal = Calendar(cal_content.decode('iso-8859-1'))
        Fixture.get_upcoming().delete()
        for event in cal.events:
            fixture = Fixture()
            splits = event.name.split('-')
            competition_name = splits[1].strip()
            if competition_name == u'English Barclays Premier League':
                competition = Competition.objects.get(name='English Premier League')
            else:
                try:
                    competition = Competition.objects.get(name=competition_name)
                except Competition.DoesNotExist:
                    raise Exception('Please add a competition with name : ' + competition_name)
            try:
                competition_year = CompetitionYear.objects.get(competition=competition, year=year)
            except CompetitionYear.DoesNotExist:
                # raise Exception('Please add a competition year with name and year : ' + competition_name + ' , ' + year)
                competition_year = CompetitionYear.objects.create(competition=competition, year=year)
            fixture.competition_year = competition_year
            if splits[0][:17] == 'Manchester United':
                fixture.is_home_game = True
                opponent_team_name = splits[0][21:].strip()
            else:
                fixture.is_home_game = False
                opponent_team_name = splits[0].strip()[:-21]
            try:
                opponent_team = Team.get(opponent_team_name)
            except Team.DoesNotExist:
                raise Exception('Please add a team with name : ' + opponent_team_name)
            fixture.opponent = opponent_team
            fixture.datetime = event.begin.datetime
            fixture.venue = event.location.split('-')[1].strip()
            fixture.save()

    @classmethod
    def save(cls):
        pass
