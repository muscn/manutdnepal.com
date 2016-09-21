from rest_framework import viewsets
from apps.stats.models import Fixture
from apps.stats.serializers import FixtureSerializer


class FixtureViewSet(viewsets.ModelViewSet):
    serializer_class = FixtureSerializer
    queryset = Fixture.objects.all()