from muscn.utils.forms import HTML5BootstrapModelForm
from .models import BankDeposit, Payment, BankAccount


class BankDepositForm(HTML5BootstrapModelForm):
    class Meta:
        model = BankDeposit
        exclude = ('payment', )

    def __init__(self, *args, **kwargs):
        super(BankDepositForm, self).__init__(*args, **kwargs)
        self.fields['bank'].empty_label = None


class PaymentForm(HTML5BootstrapModelForm):
    class Meta:
        model = Payment

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['user'].empty_label = None
        self.fields['user'].widget.choices = self.fields['user'].choices


class BankAccountForm(HTML5BootstrapModelForm):
    class Meta:
        model = BankAccount