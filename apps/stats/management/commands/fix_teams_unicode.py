# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from apps.stats.models import Team
from muscn.utils.helpers import fix_unicode


class Command(BaseCommand):
    help = 'Fix broken unicode chars in team names and fields'

    def handle(self, *args, **options):
        teams = Team.objects.all()
        for team in teams:
            team.name = fix_unicode(team.name)
            team.alternative_names = fix_unicode(team.alternative_names)
            team.save()
