from django.utils import timezone
from rest_framework import viewsets, mixins
from rest_framework.decorators import list_route
from rest_framework.response import Response

from apps.stats.models import Fixture, get_top_scorers_summary, Injury, Player, SeasonData, Competition
from ..stats.serializers import FixtureSerializer, RecentResultSerializer, InjurySerializer, PlayerSerializer, \
    SeasonDataSerializer, FixtureDetailSerializer


class FixtureViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = FixtureSerializer
    queryset = Fixture.objects.filter(datetime__gt=timezone.now()).order_by('datetime').select_related()

    def finalize_response(self, request, *args, **kwargs):
        response = super().finalize_response(request, *args, **kwargs)
        if self.request.user.is_authenticated:
            response['status'] = request.user.status
        return response

    @list_route()
    def epl_matchweek(self, request):
        # Change dict keys from date to str
        return Response({str(key): val for key, val in Competition.get('epl').matchweek.items()})


class FixtureDetailViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = FixtureDetailSerializer
    queryset = Fixture.objects.all()


class RecentResultViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = RecentResultSerializer
    queryset = Fixture.objects.filter(datetime__lt=timezone.now()).order_by('-datetime')[0:8].select_related()


class LeagueTableViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Fixture.objects.none()

    def list(self, request):
        return Response(Competition.get('epl').table)


class TopScorerViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
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


class SquadViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.filter(active=True)


class PastSeasonViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = SeasonDataSerializer
    queryset = SeasonData.objects.all()
