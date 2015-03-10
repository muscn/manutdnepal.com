from django.views.generic import DetailView
from django.views.generic.list import ListView

from apps.events.models import Event


class EventsList(ListView):
    queryset = Event.objects.filter(enabled=True).order_by('-start')


class EventDetail(DetailView):
    queryset = Event.objects.filter(enabled=True)