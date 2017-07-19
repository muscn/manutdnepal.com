AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = '/renew/'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_USERNAME_BLACKLIST = ['united', 'manutd', 'manchester', 'reddevil', 'reddevils', 'manchesterunited', 'mufc',
                              'administrator', 'admin']
ACCOUNT_FORMS = {'signup': 'apps.users.forms.SignupForm'}
SOCIALACCOUNT_AUTO_SIGNUP = False

SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
        {
            'SCOPE': ['email', 'user_birthday', 'user_website'],
            # 'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
            'METHOD': 'oauth2',
            # 'LOCALE_FUNC': 'path.to.callable',
            'VERIFIED_EMAIL': False
        }
    }
