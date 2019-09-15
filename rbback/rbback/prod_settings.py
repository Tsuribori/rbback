from rbback.settings import *
from get_docker_secret import get_docker_secret

SECRET_KEY = get_docker_secret('SECRET_KEY', autocast_name=False)

DEBUG = False

ALLOWED_HOSTS = ['localhost']

USE_X_FORWARDED_HOST = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rbback',
        'USER': 'rbback',
        'PASSWORD': get_docker_secret(
            'postgres_password', autocast_name=False),
        'HOST': 'database',
        'PORT': '5432',
        'TEST': {
            'NAME': 'test_rbback',
        },
    }
}