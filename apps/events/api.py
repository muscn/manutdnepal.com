from rest_framework import viewsets, mixins
from apps.events.models import Event
from apps.events.serializers import EventSerializer

from apps.key.permissions import DistributedKeyAuthentication


class EventViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.filter(enabled=True).order_by('-start').prefetch_related('albums')
    permission_classes = (DistributedKeyAuthentication,)
