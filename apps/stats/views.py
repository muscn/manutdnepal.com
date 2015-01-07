from django.views.generic import ListView
from muscn.utils.mixins import CreateView
from .models import Injury


class InjuryListView(ListView):
    model = Injury

