# Configuration for fargo.
# # You can override Fargo default settings here
#
# # Fargo is a Django application: for the full list of settings and their
# # values, see https://docs.djangoproject.com/en/1.7/ref/settings/
# # For more information on settings see
# # https://docs.djangoproject.com/en/1.7/topics/settings/
#
# # WARNING! Quick-start development settings unsuitable for production!
# # See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/
#
# # This file is sourced by "execfile" from /usr/lib/fargo/debian_config.py
#
# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
# TEMPLATE_DEBUG = False

ADMINS = (
  ('Admins IMIO', 'admints@example.net'),
)

# ALLOWED_HOSTS must be correct in production!
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    'local-documents.example.net',
]

# Databases
# Default: a local database named "combo"
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# Warning: don't change ENGINE
DATABASES['default']['NAME'] = 'fargo'
DATABASES['default']['USER'] = 'postgres'
DATABASES['default']['PASSWORD'] = 'password'
DATABASES['default']['HOST'] = 'database'
DATABASES['default']['PORT'] = '5432'

CACHES = {
    'default': {
        'BACKEND': 'hobo.multitenant.cache.TenantCache',
        'REAL_BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '172.17.0.1:11211',
    }
}

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Brussels'

# Email configuration
EMAIL_SUBJECT_PREFIX = '[combo local-documents]'
SERVER_EMAIL = 'fargo@example.net'
DEFAULT_FROM_EMAIL = 'fargo@example.net'

# SMTP configuration
EMAIL_HOST = 'localhost'
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 25

# HTTPS Security
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
# SESSION_COOKIE_SECURE = True

import os
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}
