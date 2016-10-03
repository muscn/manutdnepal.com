from rest_framework import serializers
from apps.stats.models import Fixture, Injury


class FixtureSerializer(serializers.ModelSerializer):
    is_today = serializers.ReadOnlyField()

    class Meta:
        model = Fixture
        depth = 2


class RecentResultSerializer(serializers.ModelSerializer):
    opponent_name = serializers.ReadOnlyField(source='opponent.not_so_long_name')
    opponent_crest = serializers.SerializerMethodField()
    opponent_short_name = serializers.ReadOnlyField(source='opponent.short_name')
    competition_name = serializers.ReadOnlyField(source='competition_year.competition.name')

    class Meta:
        model = Fixture
        fields = ('is_home_game', 'opponent_name', 'mufc_score', 'venue', 'opponent_score', 'opponent_crest', 'opponent_short_name', 'competition_name',)

    def get_opponent_crest(self, obj):
        if obj.opponent.crest:
            return obj.opponent.crest.url
        return None

class InjurySerializer(serializers.ModelSerializer):
    player_name = serializers.ReadOnlyField(source='player.name')

    class Meta:
        model = Injury
