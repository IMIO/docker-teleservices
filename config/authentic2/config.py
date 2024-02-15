# Configuration for authentic.
# You can override Authentic default settings here

# Authentic is a Django application: for the full list of settings and their
# values, see https://docs.djangoproject.com/en/1.7/ref/settings/
# For more information on settings see
# https://docs.djangoproject.com/en/1.7/topics/settings/

# WARNING! Quick-start development settings unsuitable for production!
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# This file is sourced by "execfile" from
# /usr/lib/authentic2-multitenant/debian_config.py

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
# Default: a local database named "authentic"
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# Warning: don't change ENGINE
# DATABASES['default']['NAME'] = 'authentic2_multitenant'
# DATABASES['default']['USER'] = 'authentic-multitenant'
# DATABASES['default']['PASSWORD'] = '******'
# DATABASES['default']['HOST'] = 'localhost'
# DATABASES['default']['PORT'] = '5432'

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"

# Sentry / Raven configuration
# RAVEN_CONFIG = {
#    'dsn': '',
# }

# Email configuration
# EMAIL_SUBJECT_PREFIX = '[authentic] '
# SERVER_EMAIL = 'root@authentic.example.org'
# DEFAULT_FROM_EMAIL = 'webmaster@authentic.example.org'

# SMTP configuration
# EMAIL_HOST = 'localhost'
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 25

# HTTPS Security
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

# Idp
# SAML 2.0 IDP
# A2_IDP_SAML2_ENABLE = False
# CAS 1.0 / 2.0 IDP
# A2_IDP_CAS_ENABLE = False

# Authentifications
# A2_AUTH_PASSWORD_ENABLE = True
# A2_SSLAUTH_ENABLE = False
