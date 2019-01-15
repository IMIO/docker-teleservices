BROKER_URL = 'amqp://guest:guest@rabbitmq:5672/'

AGENT_HOST_PATTERNS = {
    'authentic': ['local-auth.example.net'],
    'combo': ['local.example.net', 'local-portail-agent.example.net'],
    'wcs': ['local-formulaires.example.net'],
    'fargo': ['local-documents.example.net'],
    'passerelle': ['local-passerelle.example.net'],
}

CACHES = {
    'default': {
        'BACKEND': 'hobo.multitenant.cache.TenantCache',
        'REAL_BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '172.17.0.1:11211',
    }
}
