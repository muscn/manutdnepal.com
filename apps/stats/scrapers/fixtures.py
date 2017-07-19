from ics import Calendar
from ics.parse import ParseError
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
        # url = 'http://calendar.manutd.com/Manchester_United.ics'
        # url = 'http://hackeragenda.urlab.be/events/events.ics'
        url = 'https://calendar.google.com/calendar/ical/ov0dk4m6dedaob7oqse4nrda4s%40group.calendar.google.com/public/basic.ics'
        cal_content = cls.get_url_content(url)
        if cal_content:
            cal_content = cal_content.replace('RATE:', 'RDATE:')
            cal = Calendar(cal_content.decode('iso-8859-1').replace('\n\n', ' '))
            for event in cal.events:
                dt = event.begin.datetime
                try:
                    fixture = Fixture.objects.get(datetime=dt)
                except Fixture.DoesNotExist:
                    fixture = Fixture(datetime=dt)
                except Fixture.MultipleObjectsReturned:
                    [fix.delete() for fix in Fixture.objects.filter(datetime=dt).order_by('id')[1:]]
                    fixture = Fixture.objects.get(datetime=dt)
                # get match and competition_name from description
                splits = event.description.splitlines()[0].split(' - ')
                competition_name = splits[1].strip().split('.')[0]
                if competition_name == u'English Barclays Premier League':
                    try:
                        competition = Competition.objects.get(name='English Premier League')
                    except Competition.DoesNotExist:
                        competition = Competition.objects.create(name='English Premier League', short_name='EPL')
                elif competition_name == u'English FA Cup':
                    try:
                        competition = Competition.objects.get(name='FA Cup')
                    except Competition.DoesNotExist:
                        competition = Competition.objects.create(name='FA Cup')
                else:
                    try:
                        competition = Competition.objects.get(name=competition_name)
                    except Competition.DoesNotExist:
                        # raise Exception('Please add a competition with name : ' + competition_name)
                        competition = Competition.objects.create(name=competition_name)
                # Check for pre-season matches
                year = str(get_current_season_start_year(fixture.datetime.date()))
                try:
                    competition_year = CompetitionYear.objects.get(competition=competition, year=year)
                except CompetitionYear.DoesNotExist:
                    # raise Exception('Please add a competition year with name and year : ' + competition_name + ' , ' + year)
                    competition_year = CompetitionYear.objects.create(competition=competition, year=year)
                fixture.competition_year = competition_year
                if splits[0][:17] == 'Manchester United':
                    fixture.is_home_game = True
                    opponent_team_name = splits[0][20:].strip()
                else:
                    fixture.is_home_game = False
                    opponent_team_name = splits[0][:-20].strip()
                try:
                    opponent_team = Team.get(opponent_team_name)
                except Team.DoesNotExist:
                    # raise Exception('Please add a team with name : ' + opponent_team_name)
                    opponent_team = Team.objects.create(name=opponent_team_name)
                fixture.opponent = opponent_team
                try:
                    fixture.venue = event.location.split('-')[1].strip()
                except IndexError:
                    fixture.venue = event.location

                fixture.save()

    @classmethod
    def save(cls):
        pass
