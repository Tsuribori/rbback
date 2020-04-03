import os
from rbback.settings import *

SECRET_KEY = open('/run/secrets/secret_key', 'r').read()

DEBUG = False

MAX_POSTS = 500

ALLOWED_HOSTS = [os.environ.get('HOST')]

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

# TLS/SSL
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000

# CORS
CORS_ORIGIN_ALLOW_ALL = True
