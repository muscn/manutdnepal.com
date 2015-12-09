from django.core.management.base import BaseCommand
from apps.users.models import email_birthday_users


class Command(BaseCommand):
    help = 'Send birthday emails.'

    def handle(self, *args, **options):
        email_birthday_users()
        print 'Done!'
