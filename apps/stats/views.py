from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from apps.users.models import StaffOnlyMixin
from muscn.utils.mixins import CreateView, UpdateView
from .models import Injury, Quote, SeasonData, CompetitionYearMatches, CompetitionYear
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


class SeasonDataListView(StaffOnlyMixin, ListView):
    model = SeasonData

    # def get_context_data(self, **kwargs):
    # context = super(SeasonDataListView, self).get_context_data(**kwargs)
    #     qs = self.get_queryset()
    #     epl_seasons = qs.filter(year__gt=1991).order_by('-year')
    #     pre_epl_seasons = qs.filter(year__lt=1992).order_by('-year')
    #     context['epl_seasons'] = epl_seasons
    #     context['pre_epl_seasons'] = pre_epl_seasons
    #     return context


class SeasonDataDetailView(StaffOnlyMixin, DetailView):
    model = SeasonData

    def get_object(self):
        return get_object_or_404(SeasonData, year=self.kwargs['year'])


class SeasonCompetitionView(StaffOnlyMixin, DetailView):
    model = CompetitionYearMatches

    def get_object(self):
        competition_year = get_object_or_404(CompetitionYear, year=self.kwargs['year'],
                                             competition__slug=self.kwargs['competition'])
        return get_object_or_404(CompetitionYearMatches, competition_year=competition_year)

