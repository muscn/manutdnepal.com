from apps.stats.scrapers.base import Scraper
from apps.stats.models import Team


class TeamsScraper(Scraper):
    @classmethod
    def start(cls, *args, **kwargs):
        cls.fetch_from_espn_data()
        cls.fetch_all_teams()

    @classmethod
    def fetch_from_espn_data(cls):
        cls.log('Retrieving from ESPN EPL Teams Data JSON')
        url = 'https://raw.githubusercontent.com/jokecamp/FootballData/master/EPL%201992%20-%202015/epl-teams-2013-2014.json'
        espn_data = cls.get_json_from_url(url)
        import ipdb
        ipdb.set_trace()
        if espn_data:
            teams = espn_data['sports'][0]['leagues'][0]['teams']
            for datum in teams:
                team, created = Team.objects.get_or_create(name=datum['name'])
                team.short_name = datum['abbreviation']
                team.color = datum['color']
                team.nick_name = datum['nickname']
                team.save()

    @classmethod
    def fetch_all_teams(cls):
        cls.log('Fetching all teams from compiled json')
        url = 'https://raw.githubusercontent.com/jokecamp/FootballData/master/openFootballData/teams.json'
        data = cls.get_json_from_url(url)
        if data:
            for datum in data[222:]:
                team, created = Team.objects.get_or_create(name=datum['title'])
                team.short_name = datum['code']
                if datum['synonyms']:
                    team.alternative_names = '|' + datum['synonyms'] + '|'
                # if team.short_name:
                team.save()
