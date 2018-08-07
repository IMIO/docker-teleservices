CACHES = {
    'default': {
        'BACKEND': 'hobo.multitenant.cache.TenantCache',
        'REAL_BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '172.17.0.1:11211',
    }
}

