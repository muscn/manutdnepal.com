from season_summary import SeasonDataScraper
from facup import FACupScraper
from squad import SquadScraper
from fixtures import FixturesScraper

available_scrapers = {
    'season_summary': SeasonDataScraper,
    'facup': FACupScraper,
    'squad': SquadScraper,
    'fixtures': FixturesScraper

}
