import django_filters

from muscn.utils.forms import BootstrapForm
from .models import User


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['status']
        form = BootstrapForm
