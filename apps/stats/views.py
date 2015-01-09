from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from muscn.utils.mixins import CreateView, UpdateView
from .models import Injury, Quote, SeasonData
from .forms import InjuryForm, QuoteForm


class InjuryListView(ListView):
    model = Injury


class QuoteListView(ListView):
    model = Quote


class QuoteCreateView(CreateView):
    model = Quote
    form_class = QuoteForm
    success_url = reverse_lazy('list_quotes')


class QuoteUpdateView(UpdateView):
    model = Quote
    form_class = QuoteForm
    success_url = reverse_lazy('list_quotes')


class SeasonDataListView(ListView):
    model = SeasonData

    def get_context_data(self, **kwargs):
        context = super(SeasonDataListView, self).get_context_data(**kwargs)
        qs = self.get_queryset()
        epl_seasons = qs.filter(year__gt=1991).order_by('-year')
        pre_epl_seasons = qs.filter(year__lt=1992).order_by('-year')
        context['epl_seasons'] = epl_seasons
        context['pre_epl_seasons'] = pre_epl_seasons
        return context