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
                    del row[1]
                    dct[year].append(row)

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