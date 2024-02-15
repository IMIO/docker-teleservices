# Configuration for bijoe.
# You can override Bijoe default settings here

# Bijoe is a Django application: for the full list of settings and their
# values, see https://docs.djangoproject.com/en/1.7/ref/settings/
# For more information on settings see
# https://docs.djangoproject.com/en/1.7/topics/settings/

# WARNING! Quick-start development settings unsuitable for production!
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# This file is sourced by "execfile" from /usr/lib/bijoe/debian_config.py

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# ADMINS = (
#        # ('User 1', 'watchdog@example.net'),
#        # ('User 2', 'janitor@example.net'),
# )

# ALLOWED_HOSTS must be correct in production!
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    "*",
]

# Databases
# Default: a local database named "bijoe"
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# Warning: don't change ENGINE
# DATABASES['default']['NAME'] = 'bijoe'
# DATABASES['default']['USER'] = 'bijoe'
# DATABASES['default']['PASSWORD'] = '******'
# DATABASES['default']['HOST'] = 'localhost'
# DATABASES['default']['PORT'] = '5432'

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"

# Email configuration
# EMAIL_SUBJECT_PREFIX = '[bijoe] '
# SERVER_EMAIL = 'root@bijoe.example.org'
# DEFAULT_FROM_EMAIL = 'webmaster@bijoe.example.org'

# SMTP configuration
# EMAIL_HOST = 'localhost'
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 25

# HTTPS Security
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
