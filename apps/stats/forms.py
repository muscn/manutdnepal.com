from muscn.utils.forms import HTML5BootstrapModelForm
from .models import Quote, Injury, Player


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
