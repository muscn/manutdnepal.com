import facebook
from django.conf import settings

def facebook_api():
    graph = facebook.GraphAPI(access_token=settings.FB_ACCESS_TOKEN, version='2.5')
    return graph
