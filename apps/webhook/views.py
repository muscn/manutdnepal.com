from functools import wraps
import logging

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.decorators import available_attrs
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

log = logging.getLogger('muscn')


def password_required(view_func=None):
    def _wrapped_view(request, *args, **kwargs):
        if request.POST.get('passcode', False) == settings.WEBHOOK_PASSCODE:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)


@csrf_exempt
@password_required
def logger(request, request_type):
    if request_type == 'post':
        log_content = request.POST
    log.info(log_content)
    response = 'OK'
    return HttpResponse(response)
