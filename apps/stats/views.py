from collections import OrderedDict
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.core.cache import cache

from apps.users.models import StaffOnlyMixin
from muscn.utils.mixins import CreateView, UpdateView
from .models import Injury, Quote, SeasonData, CompetitionYearMatches, CompetitionYear, Player, Fixture, Goal, Competition
from .forms import QuoteForm


class InjuryListView(StaffOnlyMixin, ListView):
    model = Injury


class QuoteListView(StaffOnlyMixin, ListView):
    model = Quote


class QuoteCreateView(StaffOnlyMixin, CreateView):
    model = Quote
    form_class = QuoteForm
    success_url = reverse_lazy('list_quotes')


class QuoteUpdateView(StaffOnlyMixin, UpdateView):
    model = Quote
    form_class = QuoteForm
    success_url = reverse_lazy('list_quotes')


class SeasonDataListView(ListView):
    model = SeasonData

    # def get_context_data(self, **kwargs):
    # context = super(SeasonDataListView, self).get_context_data(**kwargs)
    # qs = self.get_queryset()
    # epl_seasons = qs.filter(year__gt=1991).order_by('-year')
    #     pre_epl_seasons = qs.filter(year__lt=1992).order_by('-year')
    #     context['epl_seasons'] = epl_seasons
    #     context['pre_epl_seasons'] = pre_epl_seasons
    #     return context


class SeasonDataDetailView(DetailView):
    model = SeasonData

    def get_object(self):
        return get_object_or_404(SeasonData, year=self.kwargs['year'])


class SeasonCompetitionView(DetailView):
    model = CompetitionYearMatches

    def get_object(self):
        competition_year = get_object_or_404(CompetitionYear, year=self.kwargs['year'],
                                             competition__slug=self.kwargs['competition'])
        return get_object_or_404(CompetitionYearMatches, competition_year=competition_year)


class SquadListView(ListView):
    queryset = Player.objects.filter(active=True)
    template_name = 'stats/squad.html'


class PlayerDetailView(DetailView):
    model = Player


def epl_table(request):
    standings = cache.get('epl_standings')
    context = {
        'standings': standings,
    }
    return render(request, 'stats/epl_table.html', context)


def scorers(request):
    from django.conf import settings

    goals = Goal.objects.all().select_related()
    competition_years = CompetitionYear.objects.all().select_related()
    competition_dct = OrderedDict()
    competitions = OrderedDict()
    for competition_year in competition_years:
        if competition_year.year == settings.YEAR:
            competition_dct[competition_year.competition_id] = 0
            competitions[competition_year.competition_id] = competition_year.competition.name
    players = OrderedDict()
    for goal in goals:
        competition_id = goal.match.competition_year.competition_id
        if goal.scorer not in players:
            players[goal.scorer] = {}
            players[goal.scorer]['competitions'] = competition_dct.copy()
            players[goal.scorer]['total'] = 0
        players[goal.scorer]['competitions'][competition_id] += 1
        players[goal.scorer]['total'] += 1
    players = OrderedDict(sorted(players.items(), key=lambda item: item[1]['total'], reverse=True))
    context = {
        'players': players,
        'competitions': competitions
    }
    return render(request, 'stats/scorers.html', context)


def fixtures(request):
    upcoming_fixtures = Fixture.get_upcoming().select_related()
    results = Fixture.results().select_related()
    context = {
        'fixtures': upcoming_fixtures,
        'results': results,
    }
    return render(request, 'stats/fixtures.html', context)
