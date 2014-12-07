from app.libr import HTML5ModelForm
from .models import BankDeposit


class BankDepositForm(HTML5ModelForm):
    class Meta:
        model = BankDeposit
        exclude = ('payment', )

    def __init__(self, *args, **kwargs):
        super(BankDepositForm, self).__init__(*args, **kwargs)
        self.fields['bank'].empty_label = None