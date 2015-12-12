from django.http import HttpResponse
from django.shortcuts import render

import logging
from django.views.decorators.csrf import csrf_exempt

log = logging.getLogger('muscn')

@csrf_exempt
def logger(request, request_type):
    if request_type == 'post':
        log_content = request.POST
    log.info(log_content)
    response = 'OK'
    return HttpResponse(response)
