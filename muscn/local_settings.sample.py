import os
from .settings import BASE_DIR

# Local
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
MEDIA_URL = '/media/'
ALLOWED_HOSTS = ['manutd.org.np', '127.0.0.1', 'localhost']

# Secrets
SECRET_KEY = '<35=0kv-7q5$otz58g^fv&o)iq&hldz60p^6%86xui%qcd1234'
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
WEBHOOK_PASSCODE = 'password'
FOOTBALL_API_KEY = 'xxx'
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

# Development
# from .settings import INSTALLED_APPS, MIDDLEWARE, TEMPLATES
#
# DEBUG = True
# TEMPLATES[0]['OPTIONS']['debug'] = True
# INSTALLED_APPS += (
#     'debug_toolbar',
# )
# DEBUG_TOOLBAR_CONFIG = {
#     'RESULTS_CACHE_SIZE': 100
# }
# MIDDLEWARE += (
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# )
# INTERNAL_IPS = ['127.0.0.1']
# DEBUG_TOOLBAR_PANELS = [
#     'debug_toolbar.panels.versions.VersionsPanel',
#     'debug_toolbar.panels.timer.TimerPanel',
#     'debug_toolbar.panels.settings.SettingsPanel',
#     'debug_toolbar.panels.headers.HeadersPanel',
#     'debug_toolbar.panels.request.RequestPanel',
#     'debug_toolbar.panels.sql.SQLPanel',
#     'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#     # 'debug_toolbar.panels.templates.TemplatesPanel',
#     'debug_toolbar.panels.cache.CachePanel',
#     'debug_toolbar.panels.signals.SignalsPanel',
#     'debug_toolbar.panels.logging.LoggingPanel',
#     'debug_toolbar.panels.redirects.RedirectsPanel',
# ]
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
