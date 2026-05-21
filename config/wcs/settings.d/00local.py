SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CACHES = {
    "default": {
        "BACKEND": "wcs.cache.WcsTenantCache",
        "REAL_BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "memcached:11211",
        "OPTIONS": {"ignore_exc": True},
    }
}
