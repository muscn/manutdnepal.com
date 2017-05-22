from django.views.generic import DetailView
from .models import Timeline


class TimelineDetail(DetailView):
    model = Timeline
