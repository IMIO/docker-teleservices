ADMINS = (("Admins IMIO", "admints@example.net"),)

ALLOWED_HOSTS = ["*"]

DATABASES["default"]["NAME"] = "chrono"
DATABASES["default"]["USER"] = "postgres"
DATABASES["default"]["PASSWORD"] = "password"
DATABASES["default"]["HOST"] = "database"
DATABASES["default"]["PORT"] = "5432"

CACHES = {
    "default": {
        "BACKEND": "hobo.multitenant.cache.TenantCache",
        "REAL_BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "memcached:11211",
        "OPTIONS": {"ignore_exc": True},
    }
}

BROKER_URL = "amqp://guest:guest@rabbitmq:5672/"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
