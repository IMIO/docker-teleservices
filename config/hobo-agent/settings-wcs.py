# It's possible to limit agents to particular applications, or particular
# hostnames, using the AGENT_HOST_PATTERNS configuration variable.
#
# The format is a dictionary with applications as keys and a list of hostnames as
# value. The hostnames can be prefixed by an exclamation mark to exclude them.
#
AGENT_HOST_PATTERNS = {
    'wcs': ['local-formulaires.example.net'],
}

WCS_MANAGE_COMMAND = '/usr/bin/wcsctl -f /etc/wcs/wcs-au-quotidien.cfg'

BROKER_URL = 'amqp://teleservices:password@rabbitmq:5672//teleservices'
