import datetime

from django.core.urlresolvers import reverse_lazy
from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView

from django.core.cache import cache

from apps.users.models import StaffOnlyMixin, group_required
from muscn.utils.mixins import CreateView, UpdateView, DeleteView
from .models import Injury, Quote, SeasonData, CompetitionYearMatches, CompetitionYear, Player, Fixture, \
    get_top_scorers, Goal
from .forms import QuoteForm, InjuryForm, ResultForm, GoalForm, FixtureForm, ResultGoalFormset


class InjuryListView(StaffOnlyMixin, ListView):
    model = Injury


class InjuryCreateView(StaffOnlyMixin, CreateView):
    model = Injury
    form_class = InjuryForm
    success_url = reverse_lazy('list_injuries')


class InjuryUpdateView(StaffOnlyMixin, UpdateView):
    model = Injury
    form_class = InjuryForm
    success_url = reverse_lazy('list_injuries')


class InjuryDeleteView(StaffOnlyMixin, DeleteView):
    model = Injury
    success_url = reverse_lazy('list_injuries')


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


class QuoteDeleteView(StaffOnlyMixin, DeleteView):
    model = Quote
    success_url = reverse_lazy('list_quotes')


class ResultListView(StaffOnlyMixin, ListView):
    model = Fixture
    queryset = Fixture.results()
    template_name = 'stats/result_list.html'


class ResultUpdateView(StaffOnlyMixin, UpdateView):
    model = Fixture
    # queryset = Fixture.results()
    form_class = ResultForm
    success_url = reverse_lazy('list_results')
    template_name = 'stats/result_form.html'

    def get_context_data(self, **kwargs):
        data = super(ResultUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['goal_formset'] = ResultGoalFormset(self.request.POST, instance=self.object)
        else:
            data['goal_formset'] = ResultGoalFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        goal_formset = context['goal_formset']
        self.object = form.save()
        if goal_formset.is_valid():
            goal_formset.match = self.object
            goal_formset.save()

        return super(ResultUpdateView, self).form_valid(form)


class FixtureListView(StaffOnlyMixin, ListView):
    model = Fixture
    queryset = Fixture.get_upcoming()


class FixtureUpdateView(StaffOnlyMixin, UpdateView):
    model = Fixture
    queryset = Fixture.get_upcoming()
    form_class = FixtureForm
    success_url = reverse_lazy('list_fixtures')


class GoalListView(StaffOnlyMixin, ListView):
    model = Goal


class GoalCreateView(StaffOnlyMixin, CreateView):
    model = Goal
    form_class = GoalForm
    success_url = reverse_lazy('list_goals')


class GoalUpdateView(StaffOnlyMixin, UpdateView):
    model = Goal
    form_class = GoalForm
    success_url = reverse_lazy('list_goals')


class GoalDeleteView(StaffOnlyMixin, DeleteView):
    model = Goal
    success_url = reverse_lazy('list_goals')


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
    queryset = Player.objects.filter(active=True).prefetch_related('social_accounts')
    template_name = 'stats/squad.html'


class PlayerDetailView(DetailView):
    model = Player
    queryset = Player.objects.prefetch_related(
        Prefetch('goals', queryset=Goal.objects.all().select_related('match__opponent', 'match__competition_year__competition')),
        Prefetch('assists', queryset=Goal.objects.all().select_related('match__opponent', 'match__competition_year__competition'))
    )


def epl_table(request):
    standings = cache.get('epl_standings')
    context = {
        'standings': standings,
    }
    return render(request, 'stats/epl_table.html', context)


def matchweek(request):
    standings = cache.get('epl_standings')
    context = {
        'standings': standings,
    }
    return render(request, 'stats/matchweek.html', context)


def scorers(request):
    context = get_top_scorers()
    return render(request, 'stats/scorers.html', context)


def injuries(request):
    context = {
        'current_injuries': Injury.get_current_injuries(),
        'past_injuries': Injury.get_past_injuries(),
    }
    return render(request, 'stats/injuries.html', context)


def fixtures(request):
    upcoming_fixtures = Fixture.get_upcoming().select_related('opponent', 'competition_year__competition')
    results = Fixture.results().select_related('opponent', 'competition_year__competition')
    context = {
        'fixtures': upcoming_fixtures,
        'results': results,
    }
    return render(request, 'stats/fixtures.html', context)


def all_results(request):
    context = {
        'results': Fixture.all_results().select_related('opponent', 'competition_year__competition'),
    }
    return render(request, 'stats/all_results.html', context)


@group_required('Staff')
def scrape(request, slug):
    from apps.stats.scrapers import available_scrapers

    if slug not in available_scrapers:
        raise Http404("Scraper does not exist")
    scraper = available_scrapers[slug]
    scraper.start()
    context = {
        'logs': scraper.logs,
        'old_logs': scraper.old_logs,
        'scraper': slug,
    }
    return render(request, 'stats/scraped.html', context)


class FixtureDetail(DetailView):
    model = Fixture

    def get_object(self, queryset=None):
        date = datetime.datetime.strptime(self.kwargs['date'], '%Y-%m-%d').date()
        qs = self.model.select().prefetch_related('goals__scorer', 'goals__assist_by').filter(datetime__year=date.year,
                                                                                              datetime__month=date.month,
                                                                                              datetime__day=date.day)
        try:
            fixture = get_object_or_404(qs)
        except Fixture.MultipleObjectsReturned:
            fixture = qs.first()
            qs.exclude(pk=fixture.pk).delete()
        return fixture
