import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',

    'froala_editor',
    'dbsettings',
    'linaro_django_pagination',
    'webstack_django_sorting',
    'auditlog',
    'smuggler',
    'sorl.thumbnail',
    'opbeat.contrib.django',
    'rest_framework',
    'rest_framework.authtoken',
    'solo',
    'fcm',

    'apps.core',
    'apps.users',
    'apps.payment',
    'apps.page',
    'apps.dashboard',
    'apps.stats',
    'apps.events',
    'apps.post',
    'apps.partner',
    'apps.team',
    'apps.timeline',
    'apps.webhook',
    'apps.gallery',
    'apps.key',
    'apps.push_notification',
)

MIDDLEWARE_CLASSES = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'linaro_django_pagination.middleware.PaginationMiddleware',
    'webstack_django_sorting.middleware.SortingMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',

)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.static',
                'django.core.context_processors.request',
                'django.core.context_processors.media',
                # 'django.core.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',

                'django.template.context_processors.request',
            ],
        },
    },
]

DEFAULT_FROM_EMAIL = 'webmaster@manutd.org.np'
ROOT_URLCONF = 'muscn.urls'
WSGI_APPLICATION = 'muscn.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    )
}

from user_settings import *  # noqa

try:
    from .local_settings import *  # noqa
except ImportError:
    pass


# DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# SESSION_CACHE_ALIAS = 'default'

# CACHE_MIDDLEWARE_SECONDS = 216000
# CACHE_MIDDLEWARE_KEY_PREFIX = ''

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

ESEWA_SCD = 'manutd'

# YEAR = 2015

import re

IGNORABLE_404_URLS = [
    re.compile(r'^/apple-touch-icon.*\.png$'),
]

FCM_APIKEY = "AAAAmVB3Xyo:APA91bErbKY5vOPrQaOz1tYx6VoyV34xg7FXt-lvEDBa98S11Ld0y5LPlElmT59126JLlUH77XFG8lJjAC9PgR7wI6bmpTQAmwQ2o_o6Gi5cHk7qPqAR8yiFW00Xo8XYj5mwz5Zch5LgBuGO2BNi4LtBsBG6_6lfWQ"

FCM_MAX_RECIPIENTS = 10000

ALIASES = [
    'Manchester United',
    'Man Utd',
    'Man United',
    'MUFC',
]
