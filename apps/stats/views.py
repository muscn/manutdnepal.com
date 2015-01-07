from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from muscn.utils.mixins import CreateView
from .models import Injury, Quote


class InjuryListView(ListView):
    model = Injury


class QuoteListView(ListView):
    model = Quote


class QuoteCreateView(CreateView):
    model = Quote
    success_url = reverse_lazy('list_quotes')