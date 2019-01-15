# Configuration for chrono.
# You can override Welco default settings here

# Welco is a Django application: for the full list of settings and their
# values, see https://docs.djangoproject.com/en/1.7/ref/settings/
# For more information on settings see
# https://docs.djangoproject.com/en/1.7/topics/settings/

# WARNING! Quick-start development settings unsuitable for production!
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# This file is sourced by "execfile" from /usr/lib/chrono/debian_config.py

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#ADMINS = (
#        # ('User 1', 'watchdog@example.net'),
#        # ('User 2', 'janitor@example.net'),
#)

# ALLOWED_HOSTS must be correct in production!
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
        '*',
]

# Databases
# Default: a local database named "chrono"
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# Warning: don't change ENGINE
# DATABASES['default']['NAME'] = 'chrono'
# DATABASES['default']['USER'] = 'chrono'
# DATABASES['default']['PASSWORD'] = '******'
# DATABASES['default']['HOST'] = 'localhost'
# DATABASES['default']['PORT'] = '5432'

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'

# Email configuration
# EMAIL_SUBJECT_PREFIX = '[chrono] '
# SERVER_EMAIL = 'root@chrono.example.org'
# DEFAULT_FROM_EMAIL = 'webmaster@chrono.example.org'

# SMTP configuration
# EMAIL_HOST = 'localhost'
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 25

# HTTPS Security
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
