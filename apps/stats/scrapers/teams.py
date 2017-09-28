from apps.stats.scrapers.base import Scraper
from apps.stats.models import Team


class TeamsScraper(Scraper):
    def start(self, *args, **kwargs):
        self.fetch_from_espn_data()
        self.fetch_all_teams()

    def fetch_from_espn_data(self):
        self.log('Retrieving from ESPN EPL Teams Data JSON')
        url = 'https://raw.githubusercontent.com/jokecamp/FootballData/master/EPL%201992%20-%202015/epl-teams-2013-2014.json'
        espn_data = self.get_json_from_url(url)
        if espn_data:
            teams = espn_data['sports'][0]['leagues'][0]['teams']
            for datum in teams:
                team, created = Team.objects.get_or_create(name=datum['name'])
                team.short_name = datum['abbreviation']
                team.color = datum['color']
                team.nick_name = datum['nickname']
                team.save()

    def fetch_all_teams(self):
        self.log('Fetching all teams from compiled json')
        url = 'https://raw.githubusercontent.com/jokecamp/FootballData/master/openFootballData/teams.json'
        data = self.get_json_from_url(url)
        if data:
            for datum in data[222:]:
                team, created = Team.objects.get_or_create(name=datum['title'])
                team.short_name = datum['code']
                if datum['synonyms']:
                    team.alternative_names = '|' + datum['synonyms'] + '|'
                # if team.short_name:
                team.save()
