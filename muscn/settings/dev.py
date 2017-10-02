from .base import *

DEBUG = True
ALLOWED_HOSTS = ['manutd.org.np', '127.0.0.1', 'localhost', '192.168.0.143']
SECRET_KEY = 'xxxx'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'muscn3',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}

STATIC_URL = '/static/'

INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions',
)

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATES[0]['OPTIONS']['debug'] = True


INTERNAL_IPS = ['127.0.0.1']

DEBUG_TOOLBAR_CONFIG = {
    'RESULTS_CACHE_SIZE': 100
}

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    # 'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# TEMPLATE_DEBUG = True

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'