from django.shortcuts import render
from apps.team.models import Player, Staff


def football_team(request):
    players = Player.objects.filter(active=True).select_related('user__membership')
    staffs = Staff.objects.filter(active=True).select_related('user__membership')
    context = {
        'players': players,
        'staffs': staffs,
    }
    return render(request, 'team/team.html', context)
