# -*- coding: utf-8 -*-
# Configuration for authentic.
# You can override Authentic default settings here

# Authentic is a Django application: for the full list of settings and their
# values, see https://docs.djangoproject.com/en/1.7/ref/settings/
# For more information on settings see
# https://docs.djangoproject.com/en/1.7/topics/settings/

# WARNING! Quick-start development settings unsuitable for production!
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# This file is sourced by "execfile" from /usr/lib/authentic/debian_config.py

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = (
  ('Admins IMIO', 'admints@imio.be'),
)

# ALLOWED_HOSTS must be correct in production!
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    'local-auth.example.net',
]

# Databases
# Default: a local database named "authentic"
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# Warning: don't change ENGINE
DATABASES['default']['NAME'] = 'authentic2'
DATABASES['default']['USER'] = 'postgres'
DATABASES['default']['PASSWORD'] = 'password'
DATABASES['default']['HOST'] = 'database'
DATABASES['default']['PORT'] = '5432'


LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Brussels'

# Sentry / Raven configuration
#RAVEN_CONFIG = {
#    'dsn': '',
#}

# Email configuration
EMAIL_SUBJECT_PREFIX = '[authentic local_authentic2]'
SERVER_EMAIL = 'authentic2@example.net'
DEFAULT_FROM_EMAIL = 'authentic2@example.net'

# SMTP configuration
EMAIL_HOST = 'localhost'
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
#EMAIL_PORT = 25

# HTTPS Security
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Idp
# SAML 2.0 IDP
A2_IDP_SAML2_ENABLE = True
# CAS 1.0 / 2.0 IDP
#A2_IDP_CAS_ENABLE = False
# OpenID 1.0 / 2.0 IDP
#A2_IDP_OPENID_ENABLE = False
MELLON_ADAPTER = ('authentic2_auth_fedict.adapters.AuthenticAdapter',)

# Authentifications
#A2_AUTH_PASSWORD_ENABLE = True
#A2_SSLAUTH_ENABLE = False

HOBO_ROLE_EXPORT = True
