from users.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from api.serializers import UserSerializer


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def users(request, id=None):
    many = True
    if id:
        user_object = User.objects.get(id=id)
        many = False
    else:
        user_object = User.objects.all()

    if request.method == "GET":
        serializer = UserSerializer(user_object, many=many)
        return JSONResponse(serializer.data)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

    elif request.method in ["PATCH", "PUT"]:
        data = JSONParser().parse(request)
        serializer = UserSerializer(user_object, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)

        return JSONResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        user_object.delete()
        return HttpResponse(status=204)


def index(request):
    return HttpResponse('This is api index')
