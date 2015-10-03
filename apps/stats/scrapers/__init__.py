from season_summary import SeasonDataScraper
from facup import FACupScraper
from squad import SquadScraper
from fixtures import FixturesScraper
from teams import TeamsScraper
from table import TableScraper
from tv import TVScraper

available_scrapers = {
    'season_summary': SeasonDataScraper,
    'facup': FACupScraper,
    'squad': SquadScraper,
    'fixtures': FixturesScraper,
    'teams': TeamsScraper,
    'table': TableScraper,
    'tv': TVScraper,
}
