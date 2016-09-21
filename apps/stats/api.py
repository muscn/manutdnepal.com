from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from apps.key.permissions import DistributedKeyAuthentication

from apps.stats.models import Fixture, get_latest_epl_standings, get_top_scorers_summary, Injury
from apps.stats.serializers import FixtureSerializer, RecentResultSerializer, InjurySerializer


class FixtureViewSet(viewsets.ModelViewSet):
    serializer_class = FixtureSerializer
    queryset = Fixture.objects.all()
    permission_classes = (DistributedKeyAuthentication,)

    @list_route()
    def epl_matchweek(self, request):
        if 'epl_standings' in cache:
            standings = cache.get('epl_standings')
        else:
            standings = get_latest_epl_standings()
        if 'matches' in standings:
            for k, v in standings.get('matches').items():
                standings.get('matches')[str(k)] = standings.get('matches').pop(k)
            standings = standings.get('matches')
        return Response(standings)


class RecentResultViewSet(viewsets.ModelViewSet):
    serializer_class = RecentResultSerializer
    queryset = Fixture.recent_results()
    permission_classes = (DistributedKeyAuthentication,)


class LeagueTableViewSet(viewsets.ViewSet):
    permission_classes = (DistributedKeyAuthentication,)

    def list(self, request):
        if 'epl_standings' in cache:
            standings = cache.get('epl_standings')
        else:
            standings = get_latest_epl_standings()
        if 'teams' in standings:
            standings = standings.get('teams')
        return Response(standings)


class TopScorerViewSet(viewsets.ViewSet):
    permission_classes = (DistributedKeyAuthentication,)

    def list(self, request):
        top_scorers = get_top_scorers_summary()
        top_scorers_list = []
        for k, v in top_scorers.items():
            dct = dict(name=str(k), score=v)
            top_scorers_list.append(dct)
        return Response(top_scorers_list)


class InjuryViewSet(viewsets.ModelViewSet):
    serializer_class = InjurySerializer
    queryset = Injury.get_current_injuries()
    permission_classes = (DistributedKeyAuthentication,)