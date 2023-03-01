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

SITE_HOST = '127.0.0.1:8000'
DEFAULT_FROM_EMAIL = 'IDCP <hasretkalhan@gmail.com>'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = 'hasretkalhan@gmail.com'
EMAIL_HOST_USER = 'hasretkalhan@gmail.com'
EMAIL_HOST_PASSWORD = 'ehckensyqhwiwxbd'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
PASSWORD_RESET_TIMEOUT = 14400

LOGIN_REDIRECT_URL = 'login'