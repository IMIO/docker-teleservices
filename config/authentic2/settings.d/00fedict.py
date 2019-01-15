A2_AUTH_SAML_ENABLE = False
A2_AUTH_FEDICT_ENABLE = True

MELLON_LOGIN_URL = "fedict-login"
MELLON_PUBLIC_KEYS =  ["/var/lib/authentic2-multitenant/tenants/local-auth.example.net/saml.crt"]
MELLON_PRIVATE_KEY =  "/var/lib/authentic2-multitenant/tenants/local-auth.example.net/saml.key"

MELLON_IDENTITY_PROVIDERS =  [
    {
        "METADATA_URL": "https://iamapps-public.int.belgium.be/saml/fas-metadata.xml"
    }
]

MELLON_ATTRIBUTE_MAPPING =  {
    "last_name": "{attributes[surname][0]}",
    "first_name": "{attributes[givenName][0]}"
}
