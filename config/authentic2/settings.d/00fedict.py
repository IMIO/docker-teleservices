if "authentic2_auth_fedict" not in INSTALLED_APPS:
    INSTALLED_APPS += ("authentic2_auth_fedict",)
if "authentic2_auth_fedict" not in TENANT_APPS:
    TENANT_APPS += ("authentic2_auth_fedict",)
if "authentic2_auth_fedict.backends.FedictBackend" not in AUTHENTICATION_BACKENDS:
    AUTHENTICATION_BACKENDS += ("authentic2_auth_fedict.backends.FedictBackend",)

A2_AUTH_SAML_ENABLE = True
A2_AUTH_FEDICT_ENABLE = False

MELLON_PUBLIC_KEYS = ["/var/lib/authentic2-multitenant/tenants/authentic.dev.publik.love/saml.crt"]
MELLON_PRIVATE_KEY = "/var/lib/authentic2-multitenant/tenants/authentic.dev.publik.love/saml.key"
