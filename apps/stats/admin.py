from django.contrib import admin

from .models import Injury, Competition, CompetitionYear, City, Quote, SeasonData, CompetitionYearMatches, Player, \
    Fixture, Team, Stadium


admin.site.register(Injury)
admin.site.register(Competition)
admin.site.register(CompetitionYear)
admin.site.register(City)
admin.site.register(Quote)
admin.site.register(SeasonData)
admin.site.register(CompetitionYearMatches)
admin.site.register(Player)
# admin.site.register(Fixture)
admin.site.register(Team)
admin.site.register(Stadium)

class FixtureAdmin(admin.ModelAdmin):
    model = Fixture

admin.site.register(Fixture, FixtureAdmin)