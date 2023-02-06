from .base import *

STATICFILES_DIRS = (os.path.join('static'), )

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env('POSTGRES_DB', 'postgres'),
        'USER': get_env('POSTGRES_USER', 'postgres'),
        'PASSWORD': get_env('POSTGRES_PASSWORD', 'postgres'),
        'HOST': 'localhost',
        'DISABLE_SERVER_SIDE_CURSORS': True,

    }
}
redis_url = "redis://localhost:6379/"

BROKER_URL = redis_url + "0"

CELERY_BROKER_URL = BROKER_URL
CELERY_RESULT_BACKEND = BROKER_URL

AUTH_USER_MODEL = 'authentication.User'