import requests
import json
from django.conf import settings
from rest_framework import serializers


class FacebookAPI(object):
    access_token = None
    base_url = 'https://graph.facebook.com/'
    token_url = 'https://graph.facebook.com/oauth/access_token'
    endpoints = {
        'self-details': '/me',
    }

    def __init__(self, access_token=None):
        self.access_token = access_token

    def get_user_token(self, code, redirect_url):
        payload = {'client_id': settings.FACEBOOK_CLIENT_ID, 'client_secret': settings.FACEBOOK_CLIENT_SECRET,
                   'grant_type': 'authorization_code', 'redirect_uri': redirect_url, 'code': code}
        response = requests.post(self.token_url, data=payload)
        if response.ok:
            content = json.loads(response.text)
            self.access_token = content.get('access_token')
            return self.access_token
        else:
            raise serializers.ValidationError(json.loads(response.text).get('error').get('message'))

    def request(self, endpoint, params={}):
        if not self.access_token:
            raise requests.HTTPError('Access token must be set before making api requests.')
        url = self.base_url + endpoint
        params['access_token'] = self.access_token
        # params['sig'] = self.generate_sig(endpoint, params)
        response = requests.get(url, params=params)
        if response.ok:
            content = json.loads(response.text)
            return content
        else:
            raise serializers.ValidationError(json.loads(response.text).get('error').get('message'))

    def get_self_details(self):
        endpoint = self.endpoints['self-details']
        return self.request(endpoint)
