import csv

from .base import Scraper
from apps.stats.models import Competition, CompetitionYear, CompetitionYearMatches


class FACupScraper(Scraper):
    url = 'https://raw.githubusercontent.com/jalapic/engsoccerdata/master/data-raw/facup.csv'
    local_path = '/tmp/facup.csv'
    club = 'Manchester United'

    def scrape(self):
        self.download_if_required()
        with open(self.local_path, 'rt') as csvfile:
            reader = csv.reader(csvfile)
            dct = {}
            for row in reader:
                if self.club in row[2] or self.club in row[3]:
                    year = row[1]
                    if not year in dct:
                        dct[year] = []
                    if self.club in row[2]:
                        ha = 'H'
                        opponent = row[3]
                    else:
                        ha = 'A'
                        opponent = row[2]
                    datum = {'date': row[0], 'ha': ha, 'opponent': opponent, 'hg': row[5], 'ag': row[6],
                             'round': row[7]}
                    if row[5] == 'NA':
                        datum['result'] = row[4]
                    if row[8].startswith('replay'):
                        datum['tie'] = row[8]
                    if row[9] == 'yes':
                        datum['et'] = True
                    if row[9] == 'yes':
                        datum['hp'] = row[12]
                        datum['ap'] = row[13]
                    if row[14] != 'NA':
                        datum['venue'] = row[14]
                    if row[15] != 'NA':
                        datum['attendance'] = row[15]
                    if row[16] != 'NA':
                        datum['nonmatch'] = row[16]
                    if row[17] != 'NA':
                        datum['notes'] = row[17]
                    if row[18] == 'yes':
                        datum['neutral'] = True
                    dct[year].append(datum)

        self.data = dct

    def save(self):
        competition = Competition.objects.get(name='FA Cup')
        for season, data in self.data.items():
            competition_year, created = CompetitionYear.objects.get_or_create(year=season, competition=competition)
            if created:
                competition_year.save()
            competition_year_matches, created = CompetitionYearMatches.objects.get_or_create(
                competition_year=competition_year)
            competition_year_matches.matches_data = data
            competition_year_matches.save()
