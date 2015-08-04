from django.contrib import admin

from .models import Injury, Competition, CompetitionYear, City, Quote, SeasonData, CompetitionYearMatches, Player, \
    Fixture, Team, Stadium, MatchResult

class TeamAdmin(admin.ModelAdmin):
    search_fields = ('name', 'short_name', 'alternative_names', 'nick_name')


admin.site.register(Injury)
admin.site.register(Competition)
admin.site.register(CompetitionYear)
admin.site.register(City)
admin.site.register(Quote)
admin.site.register(SeasonData)
admin.site.register(CompetitionYearMatches)
admin.site.register(Player)
# admin.site.register(Fixture)
admin.site.register(Team, TeamAdmin)
admin.site.register(Stadium)
admin.site.register(MatchResult)

class FixtureAdmin(admin.ModelAdmin):
    model = Fixture

admin.site.register(Fixture, FixtureAdmin)