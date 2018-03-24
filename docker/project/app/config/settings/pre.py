try:
    from .base import *
except Exception as e:
    raise e

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sensor',
        'USER': 'sensor',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': 5432,
    }
}