# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from apps.stats.models import Team


def fix(st):
    if st:
        try:
            return st.encode('latin1').decode('utf8')
        except UnicodeEncodeError:
            return st
        except UnicodeDecodeError:
            return unicode(st.encode('utf8'), errors='ignore')


class Command(BaseCommand):
    help = 'Fix broken unicode chars in team names and fields'

    def handle(self, *args, **options):
        teams = Team.objects.all()
        for team in teams:
            team.name = fix(team.name)
            team.alternative_names = fix(team.alternative_names)
            team.save()
