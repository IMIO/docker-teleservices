# Configuration for bijoe.

ADMINS = (
  ('Admins IMIO', 'admints@imio.be'),
)

# ALLOWED_HOSTS must be correct in production!
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    'local-stats.example.net',
]

# Databases
# Default: a local database named "combo"
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# Warning: don't change ENGINE
DATABASES['default']['NAME'] = 'bijoe'
DATABASES['default']['USER'] = 'postgres'
DATABASES['default']['PASSWORD'] = 'password'
DATABASES['default']['HOST'] = 'database'
DATABASES['default']['PORT'] = '5432'

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Brussels'

# Email configuration
EMAIL_SUBJECT_PREFIX = '[bijoe local_bijoe]'
SERVER_EMAIL = 'bijoe@example.net'
DEFAULT_FROM_EMAIL = 'bijoe@example.net'

# SMTP configuration
EMAIL_HOST = 'localhost'
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 25

# HTTPS Security
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

