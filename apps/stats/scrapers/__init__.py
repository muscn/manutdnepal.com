from .season_summary import SeasonDataScraper
from .facup import FACupScraper
from .squad import SquadScraper
from .fixtures import FixturesScraper
from .teams import TeamsScraper
from .table import TableScraper, EPLScrape, LeagueCupScrape, FACupScrape, EuropaLeagueScrape
from .tv import TVScraper
from .injuries import InjuriesScraper

available_scrapers = {
    'season_summary': SeasonDataScraper,
    'facup': FACupScraper,
    'squad': SquadScraper,
    'fixtures': FixturesScraper,
    'teams': TeamsScraper,
    'epl_table': EPLScrape,
    'league_cup_table': LeagueCupScrape,
    'fa_cup_table': FACupScrape,
    'europa_league_table': EuropaLeagueScrape,
    'tv': TVScraper,
    'injuries': InjuriesScraper,
}
