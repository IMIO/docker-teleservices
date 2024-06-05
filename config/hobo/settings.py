# Configuration for hobo.
# You can override Hobo default settings here

# Hobo is a Django application: for the full list of settings and their
# values, see https://docs.djangoproject.com/en/1.7/ref/settings/
# For more information on settings see
# https://docs.djangoproject.com/en/1.7/topics/settings/

# WARNING! Quick-start development settings unsuitable for production!
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# This file is sourced by "execfile" from /usr/lib/hobo/debian_config.py

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
# TEMPLATE_DEBUG = False

# ADMINS = (
#        ('User 1', 'poulpe@example.org'),
#        ('User 2', 'janitor@example.net'),
# )

# ALLOWED_HOSTS must be correct in production!
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    "*",
]

# If a tenant doesn't exist, the tenant middleware raise a 404 error. If you
# prefer to redirect to a specific site, use:
# TENANT_NOT_FOUND_REDIRECT_URL = 'http://www.example.net/'

# Databases
# Default: a local database named "hobo"
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# Warning: don't change ENGINE
# DATABASES['default']['NAME'] = 'hobo'
# DATABASES['default']['USER'] = 'hobo'
# DATABASES['default']['PASSWORD'] = '******'
# DATABASES['default']['HOST'] = 'localhost'
# DATABASES['default']['PORT'] = '5432'

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"

# Email configuration
# EMAIL_SUBJECT_PREFIX = '[Hobo] '
# SERVER_EMAIL = 'root@hobo.example.org'
# DEFAULT_FROM_EMAIL = 'webmaster@hobo.example.org'

# SMTP configuration
# EMAIL_HOST = 'localhost'
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 25

# HTTPS
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
