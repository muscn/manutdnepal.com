from django.core.cache import cache
from django.utils import timezone
from rest_framework import viewsets, mixins
from rest_framework.decorators import list_route
from rest_framework.response import Response
from apps.key.permissions import DistributedKeyAuthentication

from apps.stats.models import Fixture, get_latest_epl_standings, get_top_scorers_summary, Injury, Wallpaper, Player, \
    SeasonData
from apps.stats.scrapers import EPLScrape
from ..stats.serializers import FixtureSerializer, RecentResultSerializer, InjurySerializer, WallpaperSerializer, \
    PlayerSerializer, SeasonDataSerializer, FixtureDetailSerializer


class FixtureViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = FixtureSerializer
    queryset = Fixture.objects.filter(datetime__gt=timezone.now()).order_by('datetime').select_related()
    permission_classes = []

    @list_route()
    def epl_matchweek(self, request):
        if 'epl_standings' in cache:
            standings = cache.get('epl_standings')
        else:
            EPLScrape.start(command=True)
            standings = cache.get('epl_standings')
        if 'matches' in standings:
            for k, v in standings.get('matches').items():
                standings.get('matches')[str(k)] = standings.get('matches').pop(k)
            standings = standings.get('matches')
        return Response(standings)


class FixtureDetailViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = FixtureDetailSerializer
    queryset = Fixture.objects.all()
    # permission_classes = (DistributedKeyAuthentication,)



class RecentResultViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = RecentResultSerializer
    queryset = Fixture.objects.filter(datetime__lt=timezone.now()).order_by('-datetime')[0:8].select_related()
    # permission_classes = (DistributedKeyAuthentication,)


class LeagueTableViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    # permission_classes = (DistributedKeyAuthentication,)

    def list(self, request):
        if 'epl_standings' in cache:
            standings = cache.get('epl_standings')
        else:
            standings = get_latest_epl_standings()
        if 'teams' in standings:
            standings = standings.get('teams')
        return Response(standings)


class TopScorerViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    # permission_classes = (DistributedKeyAuthentication,)

    def list(self, request):
        top_scorers = get_top_scorers_summary()
        top_scorers_list = []
        for k, v in top_scorers.items():
            dct = dict(name=str(k), score=v)
            top_scorers_list.append(dct)
        return Response(top_scorers_list)


class InjuryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = InjurySerializer
    queryset = Injury.get_current_injuries()
    # permission_classes = (DistributedKeyAuthentication,)


class SquadViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.filter(active=True)
    # permission_classes = (DistributedKeyAuthentication,)


class PastSeasonViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = SeasonDataSerializer
    queryset = SeasonData.objects.all()
    # permission_classes = (DistributedKeyAuthentication,)


class WallpaperViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = WallpaperSerializer
    # permission_classes = (DistributedKeyAuthentication,)

    def get_queryset(self):
        return Wallpaper.objects.all().order_by('-pk')[:5]