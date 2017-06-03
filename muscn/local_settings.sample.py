from settings import *

import sys

DEBUG = False
ALLOWED_HOSTS = ['manutd.org.np', '127.0.0.1', 'localhost']
SITE_ID = 1
SECRET_KEY = '<35=0kv-7q5$otz58g^fv&o)iq&hldz60p^6%86xui%qcd1234'
#TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ()


DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'muscn',
         'USER': 'muscn',
         'PASSWORD': 'xxx',
         'HOST': 'localhost',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
         'PORT': '',  # Set to empty string for default.
     }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
MEDIA_URL = '/media/'

WEBHOOK_PASSCODE = 'password'

INSTALLED_APPS += (
    # 'debug_toolbar',
)

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
    }
}


FOOTBALL_API_KEY = 'xxx'
TEMPLATES[0]['OPTIONS']['debug'] = True

SERVER_EMAIL = 'manutd@awecode.com'
FB_ACCESS_TOKEN = 'xxx'
FCM_APIKEY = 'xxx'

OPBEAT = {
    'ORGANIZATION_ID': 'adsd',
    'APP_ID': 'appt_id',
    'SECRET_TOKEN': 'asd',
}

ANYMAIL = {
    "MAILGUN_API_KEY": "<your Mailgun key>",
}