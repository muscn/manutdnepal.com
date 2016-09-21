from rest_framework import serializers
from apps.stats.models import Fixture, Injury


class FixtureSerializer(serializers.ModelSerializer):
    is_today = serializers.ReadOnlyField()

    class Meta:
        model = Fixture
        depth = 1


class RecentResultSerializer(serializers.ModelSerializer):
    result = serializers.ReadOnlyField()
    score = serializers.ReadOnlyField()

    class Meta:
        model = Fixture
        fields = ('result', 'score',)


class InjurySerializer(serializers.ModelSerializer):
    class Meta:
        model = Injury
