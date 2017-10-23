import django_filters

from muscn.utils.forms import BootstrapForm
from .models import User


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['status', 'card_statuses__status', 'card_statuses__pickup_location', 'card_statuses__season']
        form = BootstrapForm
