from rest_framework import viewsets, mixins

from .models import Partner
from .serializers import PartnerSer


class PartnerViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = PartnerSer
    queryset = Partner.objects.filter(active=True)
    permission_classes = []
