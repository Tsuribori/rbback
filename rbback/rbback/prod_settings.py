from rbback.settings import *

DEBUG = False

ALLOWED_HOSTS = ['localhost', '.rasberryheaven.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': 'database',
        'PORT': '5432',
        'TEST': {
            'NAME': 'test_rbback',
        },
    }
}
