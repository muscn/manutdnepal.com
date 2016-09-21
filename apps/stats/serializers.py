from rest_framework import serializers
from apps.stats.models import Fixture


class FixtureSerializer(serializers.ModelSerializer):
    is_today = serializers.ReadOnlyField()

    class Meta:
        model = Fixture
        depth = 1
