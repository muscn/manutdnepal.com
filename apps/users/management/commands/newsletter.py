import logging

from django.core.management.base import BaseCommand
from apps.users.models import email_birthday_users, Newsletter

logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'Send newsletter.'

    def add_arguments(self, parser):
        parser.add_argument('key', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            key = options['key'][0]
            newsletter = Newsletter.objects.get(key=key)
            newsletter.send()
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
