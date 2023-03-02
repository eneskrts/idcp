from .base import *

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DEBUG = True

redis_url = "redis://idcp_redis:6379/"
BROKER_URL = redis_url + "0"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env('POSTGRES_DB', 'postgres'),
        'USER': get_env('POSTGRES_USER', 'postgres'),
        'PASSWORD': get_env('POSTGRES_PASSWORD', 'postgres'),
        'HOST': get_env('POSTGRES_CONTAINER_NAME'),
        'DISABLE_SERVER_SIDE_CURSORS': True,

    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://idcp_redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        }
    }
}

CELERY_BROKER_URL = BROKER_URL
CELERY_RESULT_BACKEND = BROKER_URL
