from django.shortcuts import render
from apps.users.models import group_required
from django.views.generic.list import ListView
from auditlog.models import LogEntry


@group_required('Staff')
def index(request):
    return render(request, 'dashboard_index.html')


class AuditLogListView(ListView):
    model = LogEntry