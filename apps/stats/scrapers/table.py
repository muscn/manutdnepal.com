from .base import Scraper
from apps.stats.models import get_latest_epl_standings

class TableScraper(Scraper):
    @classmethod
    def start(cls):
        get_latest_epl_standings()
