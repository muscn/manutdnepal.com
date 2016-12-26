from rest_framework import viewsets
from apps.events.models import Event
from apps.events.serializers import EventSerializer

from apps.key.permissions import DistributedKeyAuthentication


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.filter(enabled=True).order_by('-start').prefetch_related('albums')
    permission_classes = (DistributedKeyAuthentication,)
