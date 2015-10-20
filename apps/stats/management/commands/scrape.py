from django.core.management.base import BaseCommand, CommandError
from apps.stats.scrapers import available_scrapers


class Command(BaseCommand):
    args = '[ ' + ' | '.join(available_scrapers.keys()) + ' ]'
    help = 'Scrap and Save. That\'s what I do.'

    def handle(self, *args, **options):
        if len(args) < 1:
            raise CommandError(
                'I need something to scrap. Available arguments are: ' + ' | '.join(available_scrapers.keys()))
        for arg in args:
            scraper = available_scrapers[arg]
            scraper.start(command=True)
