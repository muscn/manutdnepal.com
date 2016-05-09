from muscn.utils.forms import HTML5BootstrapModelForm, BootstrapModelForm
from django.forms.models import inlineformset_factory

from .models import Quote, Injury, Player, Fixture, Goal


class QuoteForm(HTML5BootstrapModelForm):
    class Meta:
        model = Quote
        exclude = ()


class InjuryForm(HTML5BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        super(InjuryForm, self).__init__(*args, **kwargs)
        self.fields['player'].queryset = Player.objects.filter(active=True)

    class Meta:
        model = Injury
        exclude = ()


class ResultForm(HTML5BootstrapModelForm):
    class Meta:
        model = Fixture
        fields = ['mufc_score', 'opponent_score', 'remarks']


class FixtureForm(HTML5BootstrapModelForm):
    class Meta:
        model = Fixture
        exclude = ('competition_year', 'opponent', 'datetime')


class GoalForm(HTML5BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        super(GoalForm, self).__init__(*args, **kwargs)
        self.fields['scorer'].queryset = Player.objects.filter(active=True)
        self.fields['match'].queryset = Fixture.results()
        self.fields['match'].empty_label = None

    class Meta:
        model = Goal
        exclude = ()


class GoalInlineForm(BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        super(GoalInlineForm, self).__init__(*args, **kwargs)
        self.fields['scorer'].queryset = Player.objects.filter(active=True)

    class Meta:
        model = Goal
        exclude = ()


ResultGoalFormset = inlineformset_factory(Fixture, Goal, form=GoalInlineForm, extra=3, can_delete=True)
