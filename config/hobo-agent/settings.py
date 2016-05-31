# AMQP message broker
# http://celery.readthedocs.org/en/latest/configuration.html#broker-url
# transport://userid:password@hostname:port/virtual_host
BROKER_URL = 'amqp://guest:guest@rabbitmq:5672/'

# It's possible to limit agents to particular applications, or particular
# hostnames, using the AGENT_HOST_PATTERNS configuration variable.
#
# The format is a dictionary with applications as keys and a list of hostnames as
# value. The hostnames can be prefixed by an exclamation mark to exclude them.
#
AGENT_HOST_PATTERNS = {
    'authentic': ['local-auth.example.net'],
    'combo': ['local.example.net', 'local-portail-agent.example.net'],
    'wcs': ['local-formulaires.example.net'],
    'fargo': ['local-documents.example.net'],
}

WCS_MANAGE_COMMAND = 'sudo -u wcs-au-quotidien /usr/sbin/wcsctl -f /etc/wcs/wcs-au-quotidien.cfg'
AUTHENTIC_MANAGE_COMMAND = 'sudo -u authentic-multitenant /usr/bin/authentic2-multitenant-manage'
COMBO_MANAGE_COMMAND = 'sudo -u combo /usr/bin/combo-manage'
PASSERELLE_MANAGE_COMMAND = 'sudo -u passerelle /usr/bin/passerelle-manage'
FARGO_MANAGE_COMMAND = 'sudo -u fargo /usr/bin/fargo-manage'
WELCO_MANAGE_COMMAND = 'sudo -u welco /usr/bin/welco-manage'

