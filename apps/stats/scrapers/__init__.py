from .season_summary import SeasonDataScraper
from .facup import FACupScraper
from .squad import SquadScraper
from .fixtures import FixturesScraper
from .teams import TeamsScraper
from .leagues import LeagueScraper, AllLeagues
from .tv import TVScraper
from .injuries import InjuriesScraper

available_scrapers = {
    'season_summary': SeasonDataScraper,
    'facup': FACupScraper,
    'squad': SquadScraper,
    'fixtures': FixturesScraper,
    'teams': TeamsScraper,
    'tv': TVScraper,
    'injuries': InjuriesScraper,

    'all_leagues': AllLeagues,
}
