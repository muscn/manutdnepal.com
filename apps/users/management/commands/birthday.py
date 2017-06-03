import logging

from django.core.management.base import BaseCommand
from apps.users.models import email_birthday_users

logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'Send birthday emails.'

    def handle(self, *args, **options):
        try:
            email_birthday_users()
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
