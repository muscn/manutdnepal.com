import django_filters

from muscn.utils.forms import BootstrapForm
from .models import User

METHODS = (
    ('esewa_payment', 'E-sewa'),
    ('direct_payment', 'Direct'),
    ('bank_deposit', 'Bank'),
)


def get_payment_method(qs, name, value):
    kgs = {'payments__' + value + '__isnull': False}
    return qs.filter(**kgs).order_by('-payments__date_time')


class UserFilter(django_filters.FilterSet):
    payment_method = django_filters.ChoiceFilter(method=get_payment_method, choices=METHODS, label='Payment method')

    class Meta:
        model = User
        fields = ['status', 'payment_method', 'card_statuses__status', 'card_statuses__pickup_location', 'card_statuses__season']
        form = BootstrapForm
