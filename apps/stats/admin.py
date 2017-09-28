from django.contrib import admin
from django import forms
from django.contrib.admin import SimpleListFilter
from django.utils import timezone

from muscn.utils.mixins import EmptyFilterSpec
from .models import Injury, Competition, CompetitionYear, City, Quote, SeasonData, Player, Fixture, Team, Goal, Stadium, \
    PlayerSocialAccount, Wallpaper


class CrestEmptyFilterSpec(EmptyFilterSpec):
    title = 'Crest'
    parameter_name = 'crest'


class TeamAdmin(admin.ModelAdmin):
    search_fields = ('name', 'short_name', 'alternative_names', 'nick_name')
    list_display = ('name', 'crest')
    list_filter = (CrestEmptyFilterSpec,)


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


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'slug', 'order', 'friendly', 'active']
    list_filter = ['friendly', 'active']


admin.site.register(Competition, CompetitionAdmin)

admin.site.register(Goal, GoalAdmin)
admin.site.register(Injury)
admin.site.register(PlayerSocialAccount)
admin.site.register(Quote)
admin.site.register(SeasonData)
admin.site.register(Team, TeamAdmin)
admin.site.register(Stadium)


class FixtureResultFilter(SimpleListFilter):
    title = 'Type'

    parameter_name = 'type'

    def lookups(self, request, model_admin):
        return (
            ('fixture', 'Fixture'),
            ('result', 'Result'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'fixture':
            return queryset.filter(datetime__gt=timezone.now())
        if self.value() == 'result':
            return queryset.exclude(datetime__gt=timezone.now())
        return queryset


class FixtureAdmin(admin.ModelAdmin):
    list_display = ('opponent', 'is_home_game', 'datetime', 'competition_year', 'venue')
    list_filter = (
        FixtureResultFilter, 'is_home_game', 'competition_year__competition', 'competition_year', 'competition_year__year')
    inlines = [GoalInline]

    def get_queryset(self, request):
        return super(FixtureAdmin, self).get_queryset(request).select_related('opponent', 'competition_year',
                                                                              'competition_year__competition')


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


class CompetitionYearAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'competition', 'year')
    list_filter = ('competition', 'year')

    def get_queryset(self, request):
        return super(CompetitionYearAdmin, self).get_queryset(request).select_related('competition')


admin.site.register(CompetitionYear, CompetitionYearAdmin)
