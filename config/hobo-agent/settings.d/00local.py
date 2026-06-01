BROKER_URL = "amqp://guest:guest@rabbitmq:5672/"

AGENT_HOST_PATTERNS = {
    "authentic": ["authentic.dev.publik.love"],
    "chrono": ["chrono.dev.publik.love"],
    "combo": ["combo.dev.publik.love", "agent-combo.dev.publik.love"],
    "wcs": ["wcs.dev.publik.love"],
    "fargo": ["local-documents.example.net"],
    "passerelle": ["passerelle.dev.publik.love"],
}

CACHES = {
    "default": {
        "BACKEND": "hobo.multitenant.cache.TenantCache",
        "REAL_BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "memcached:11211",
        "OPTIONS": {"ignore_exc": True},
    }
}
