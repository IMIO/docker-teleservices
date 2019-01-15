ADMINS = (
    ('Admins IMIO', 'admints@example.net'),
)

ALLOWED_HOSTS = ['*']

DATABASES['default']['NAME'] = 'authentic2'
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

BROKER_URL = 'amqp://guest:guest@rabbitmq:5672/'
