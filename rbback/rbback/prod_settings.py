from rbback.settings import *

SECRET_KEY = open('/run/secrets/secret_key', 'r').read()

DEBUG = False

ALLOWED_HOSTS = ['localhost']

USE_X_FORWARDED_HOST = True
X_FRAME_OPTIONS = 'DENY'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rbback',
        'USER': 'rbback',
        'PASSWORD': open(
            '/run/secrets/postgres_password', 'r').read().replace('\n', ''),
        'HOST': 'database',
        'PORT': '5432',
        'TEST': {
            'NAME': 'test_rbback',
        },
    }
}

FORCE_SCRIPT_NAME = '/api'
