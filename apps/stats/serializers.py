from rest_framework import serializers
from apps.stats.models import Fixture, Injury


class FixtureSerializer(serializers.ModelSerializer):
    is_today = serializers.ReadOnlyField()

    class Meta:
        model = Fixture
        depth = 2


class RecentResultSerializer(serializers.ModelSerializer):
    opponent_name = serializers.ReadOnlyField(source='opponent.not_so_long_name')

    class Meta:
        model = Fixture
        fields = ('is_home_game', 'opponent_name', 'mufc_score', 'opponent_score',)


class InjurySerializer(serializers.ModelSerializer):
    class Meta:
        model = Injury
