from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from muscn.utils.mixins import CreateView, UpdateView
from .models import Injury, Quote
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