from .base import Scraper
from apps.stats.models import Competition, CompetitionYear, CompetitionYearMatches
import csv


class FACupScraper(Scraper):
    url = 'https://raw.githubusercontent.com/jalapic/engsoccerdata/master/data-raw/facup.csv'
    local_path = '/tmp/facup.csv'
    club = 'Manchester United'

    @classmethod
    def scrape(cls):
        cls.download_if_required()
        with open(cls.local_path, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            dct = {}
            for row in reader:
                if cls.club in row[2] or cls.club in row[3]:
                    year = row[1]
                    if not year in dct:
                        dct[year] = []
                    if cls.club in row[2]:
                        ha = 'H'
                        opponent = row[3]
                    else:
                        ha = 'A'
                        opponent = row[2]
                    datum = {'date': row[0], 'ha': ha, 'opponent': opponent, 'hg': row[5], 'ag': row[6],
                             'round': row[7]}
                    if row[8].startswith('replay'):
                        datum['tie'] = row[8]
                    if row[8] == 'yes':
                        datum['et'] = True
                    if row[9] == 'yes':
                        datum['hp'] = row[11]
                        datum['ap'] = row[12]
                    if row[13] != 'NA':
                        datum['venue'] = row[13]
                    if row[14] != 'NA':
                        datum['attendance'] = row[14]
                    if row[15] != 'NA':
                        datum['nonmatch'] = row[15]
                    if row[16] != 'NA':
                        datum['notes'] = row[16]
                    if row[17] == 'yes':
                        datum['neutral'] = True
                    dct[year].append(datum)

        cls.data = dct


    @classmethod
    def save(cls):
        competition = Competition.objects.get(name='FA Cup')
        for season, data in cls.data.iteritems():
            competition_year, created = CompetitionYear.objects.get_or_create(year=season, competition=competition)
            if created:
                competition_year.save()
            competition_year_matches, created = CompetitionYearMatches.objects.get_or_create(
                competition_year=competition_year)
            competition_year_matches.matches_data = data
            competition_year_matches.save()