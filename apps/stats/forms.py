from muscn.utils.forms import HTML5BootstrapModelForm
from .models import Quote, Injury


class QuoteForm(HTML5BootstrapModelForm):
    class Meta:
        model = Quote
        exclude = ()


class InjuryForm(HTML5BootstrapModelForm):
    class Meta:
        model = Injury
        exclude = ()
