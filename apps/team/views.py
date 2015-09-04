from django.shortcuts import render
from apps.team.models import Player, Staff


def football_team(request):
    players = Player.objects.filter(active=True)
    staffs = Staff.objects.filter(active=True)
    context = {
        'players': players,
        'staffs': staffs,
    }
    return render(request, 'team/team.html', context)
