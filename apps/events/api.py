from rest_framework import viewsets, mixins
from apps.events.models import Event
from apps.events.serializers import EventSerializer



class EventViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.filter(enabled=True).order_by('-start').prefetch_related('albums')
