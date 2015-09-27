from settings import *

from logging import config
import sys

DEBUG = True
ALLOWED_HOSTS = []
SITE_ID = 1
SECRET_KEY = '<35=0kv-7q5$otz58g^fv&o)iq&hldz60p^6%86xui%qcd2f<3'
TEMPLATE_DEBUG = DEBUG

ADMINS = (('Admin Name', 'admin@server.com'),)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'muscn',
#         'USER': 'muscn',
#         'PASSWORD': 'muscn',
#         'HOST': 'localhost',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
#         'PORT': '',  # Set to empty string for default.
#     }
# }

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
MEDIA_URL = '/media/'


LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}
config.dictConfig(LOGGING)




INSTALLED_APPS += (
    # 'debug_toolbar',
)

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
    }
}

