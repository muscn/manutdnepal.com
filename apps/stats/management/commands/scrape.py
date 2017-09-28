import logging

from django.core.management.base import BaseCommand, CommandError
from apps.stats.scrapers import available_scrapers

logger = logging.getLogger('django')


class Command(BaseCommand):
    args = '[ ' + ' | '.join(available_scrapers.keys()) + ' ]'
    help = 'Scrap and Save. That\'s what I do.' + ' Available scrapers are: ' + ' | '.join(available_scrapers.keys())

    def add_arguments(self, parser):
        parser.add_argument('scraper', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            for arg in options['scraper']:
                try:
                    scraper = available_scrapers[arg]()
                except KeyError:
                    raise CommandError('Scraper "%s" does not exist' % arg)
                scraper.start(command=True)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
