from rest_framework import serializers

from apps.stats.models import Fixture, Injury, Wallpaper, Player, PlayerSocialAccount, SeasonData, Goal


class FixtureSerializer(serializers.ModelSerializer):
    is_today = serializers.ReadOnlyField()

    class Meta:
        model = Fixture
        depth = 2


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal


class FixtureDetailSerializer(serializers.ModelSerializer):
    opponent_name = serializers.ReadOnlyField(source='opponent.not_so_long_name')
    opponent_crest = serializers.SerializerMethodField()
    opponent_short_name = serializers.ReadOnlyField(source='opponent.short_name')
    competition_name = serializers.ReadOnlyField(source='competition_year.competition.name')
    goals = GoalSerializer(many=True)

    class Meta:
        model = Fixture
        depth = 2
        fields = ('id', 'is_home_game', 'opponent_name', 'mufc_score', 'venue', 'opponent_score', 'opponent_crest',
                  'opponent_short_name', 'competition_name', 'datetime', 'data', 'broadcast_on', 'goals')

    def get_opponent_crest(self, obj):
        if obj.opponent.crest:
            return obj.opponent.crest.url
        return None


class RecentResultSerializer(serializers.ModelSerializer):
    opponent_name = serializers.ReadOnlyField(source='opponent.not_so_long_name')
    opponent_crest = serializers.SerializerMethodField()
    opponent_short_name = serializers.ReadOnlyField(source='opponent.short_name')
    competition_name = serializers.ReadOnlyField(source='competition_year.competition.name')

    class Meta:
        model = Fixture
        fields = ('id', 'is_home_game', 'opponent_name', 'mufc_score', 'venue', 'opponent_score', 'opponent_crest',
                  'opponent_short_name', 'competition_name', 'datetime',)

    def get_opponent_crest(self, obj):
        if obj.opponent.crest:
            return obj.opponent.crest.url
        return None


class InjurySerializer(serializers.ModelSerializer):
    player_name = serializers.ReadOnlyField(source='player.name')

    class Meta:
        model = Injury


class PlayerSocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerSocialAccount


class PlayerSerializer(serializers.ModelSerializer):
    nationality = serializers.SerializerMethodField()
    social_accounts = PlayerSocialAccountSerializer(many=False)

    class Meta:
        model = Player

    def get_nationality(self, obj):
        return obj.get_nationality_display()


class SeasonDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonData


class WallpaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallpaper
