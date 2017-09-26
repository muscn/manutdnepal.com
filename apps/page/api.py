from rest_framework import viewsets, mixins

from apps.page.models import Page
from apps.page.serializers import PageSerializer


class PageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = PageSerializer
    lookup_field = 'slug'
    queryset = Page.objects.all()
