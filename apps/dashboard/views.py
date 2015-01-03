from django.shortcuts import render
from apps.users.models import group_required

@group_required('Staff')
def index(request):
    return render(request, 'dashboard_index.html')

