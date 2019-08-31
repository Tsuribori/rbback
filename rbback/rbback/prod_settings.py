from rbback.settings import *
from get_docker_secret import get_docker_secret

DEBUG = False

ALLOWED_HOSTS = ['localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rbback',
        'USER': 'rbback',
        'PASSWORD': get_docker_secret(
            'POSTGRES_PASSWORD', autocast_name=False),
        'HOST': 'database',
        'PORT': '5432',
        'TEST': {
            'NAME': 'test_rbback',
        },
    }
}
