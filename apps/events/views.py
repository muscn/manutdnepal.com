from django.views.generic.list import ListView
from apps.events.models import Event


class EventsList(ListView):
    model = Event


