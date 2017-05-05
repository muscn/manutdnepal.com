from django.contrib import admin
from django import forms

from .models import Injury, Competition, CompetitionYear, City, Quote, SeasonData, CompetitionYearMatches, Player, \
    Fixture, Team, Goal, Stadium, PlayerSocialAccount, Wallpaper


class TeamAdmin(admin.ModelAdmin):
    search_fields = ('name', 'short_name', 'alternative_names', 'nick_name')


class GoalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GoalForm, self).__init__(*args, **kwargs)
        self.fields['match'].queryset = Fixture.results()

    class Meta:
        model = Goal
        exclude = ()


class GoalInline(admin.TabularInline):
    model = Goal


class GoalAdmin(admin.ModelAdmin):
    form = GoalForm


admin.site.register(Goal, GoalAdmin)
admin.site.register(Injury)
admin.site.register(PlayerSocialAccount)
admin.site.register(Competition)
admin.site.register(CompetitionYear)
# admin.site.register(City)
admin.site.register(Quote)
admin.site.register(SeasonData)
# admin.site.register(CompetitionYearMatches)
# admin.site.register(Fixture)
admin.site.register(Team, TeamAdmin)
admin.site.register(Stadium)


# admin.site.register(MatchResult)

class FixtureAdmin(admin.ModelAdmin):
    model = Fixture
    list_display = ('opponent', 'is_home_game', 'datetime', 'competition_year', 'venue')
    list_filter = ('is_home_game', 'competition_year__competition', 'competition_year', 'competition_year__year')
    inlines = [GoalInline]


admin.site.register(Fixture, FixtureAdmin)
admin.site.register(Wallpaper)


# class ResultAdmin(admin.ModelAdmin):
#     model = Fixture
#
# admin.site.register(Fixture, ResultAdmin)

class PlayerAdmin(admin.ModelAdmin):
    list_display = ['squad_no', 'name', 'active', 'on_loan']
    list_display_links = ['squad_no', 'name']
    list_filter = ['favored_position', 'on_loan', 'active', 'nationality', ]
    search_fields = ['name']


admin.site.register(Player, PlayerAdmin)
