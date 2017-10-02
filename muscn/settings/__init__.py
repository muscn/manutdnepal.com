from .base import *

environment = os.getenv('DJANGO_ENV')
if environment == 'production':
    from .prod import *
else:
    from .env import *
