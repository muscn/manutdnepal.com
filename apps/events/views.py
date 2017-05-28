from django.views.generic import DetailView
from django.views.generic.list import ListView

from apps.events.models import Event


class EventsList(ListView):
    queryset = Event.objects.filter(enabled=True).order_by('-start').prefetch_related('albums')


class EventDetail(DetailView):
    queryset = Event.objects.filter(enabled=True).prefetch_related('albums__images')