AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = '/membership/'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_USERNAME_BLACKLIST = ['united', 'manutd', 'manchester', 'reddevil', 'reddevils', 'manchesterunited', 'mufc',
                              'administrator', 'admin']
ACCOUNT_FORMS = {
    # 'login': 'apps.users.forms.LoginForm',
    'signup': 'apps.users.forms.SignupForm'}
SOCIALACCOUNT_AUTO_SIGNUP = True
SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False
SOCIALACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_DISPLAY = 'email'
# ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'

SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
        {
            'SCOPE': ['email', 'user_birthday', ],
            # 'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
            'METHOD': 'oauth2',
            # 'LOCALE_FUNC': 'path.to.callable',
            'VERIFIED_EMAIL': False
        },
        'google': {
            'SCOPE': [
                'profile',
                'email',
            ],
            'AUTH_PARAMS': {
                'access_type': 'online',
            }
        }
    }
