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

    'apps.core',
    'apps.users',
    'apps.payment',
    'apps.page',
    'apps.dashboard',
    'apps.stats',
    'apps.events',

)

MIDDLEWARE_CLASSES = (
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

ROOT_URLCONF = 'muscn.urls'
WSGI_APPLICATION = 'muscn.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_L10N = True
USE_TZ = False

from user_settings import *  # noqa

try:
    from .local_settings import *  # noqa
except ImportError:
    pass


# DJANGO_REDIS_IGNORE_EXCEPTIONS = True

#SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
#SESSION_CACHE_ALIAS = 'default'

# CACHE_MIDDLEWARE_SECONDS = 216000
# CACHE_MIDDLEWARE_KEY_PREFIX = ''

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

ESEWA_SCD = 'manutd'
