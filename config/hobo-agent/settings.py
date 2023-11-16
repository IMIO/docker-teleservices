# AMQP message broker
# http://celery.readthedocs.org/en/latest/configuration.html#broker-url
# transport://userid:password@hostname:port/virtual_host
BROKER_URL = 'amqp://'

# It's possible to limit agents to particular applications, or particular
# hostnames, using the AGENT_HOST_PATTERNS configuration variable.
#
# The format is a dictionary with applications as keys and a list of hostnames as
# value. The hostnames can be prefixed by an exclamation mark to exclude them.
#
#  AGENT_HOST_PATTERNS = {
#      'wcs': ['*.example.net', '!  *.dev.example.net'],
#  }
#
# Will limit wcs deployments to *.example.net hostnames, while excluding
# *.dev.example.net.
AGENT_HOST_PATTERNS = None

WCS_MANAGE_COMMAND = 'sudo -u wcs /usr/bin/wcs-manage'
AUTHENTIC_MANAGE_COMMAND = 'sudo -u authentic-multitenant /usr/bin/authentic2-multitenant-manage'
COMBO_MANAGE_COMMAND = 'sudo -u combo /usr/bin/combo-manage'
PASSERELLE_MANAGE_COMMAND = 'sudo -u passerelle /usr/bin/passerelle-manage'
FARGO_MANAGE_COMMAND = 'sudo -u fargo /usr/bin/fargo-manage'
WELCO_MANAGE_COMMAND = 'sudo -u welco /usr/bin/welco-manage'
MANDAYEJS_MANAGE_COMMAND = 'sudo -u mandayejs /usr/bin/mandayejs-manage'
CHRONO_MANAGE_COMMAND = 'sudo -u chrono /usr/bin/chrono-manage'
CORBO_MANAGE_COMMAND = 'sudo -u corbo /usr/bin/corbo-manage'
PIWIK_MANAGE_COMMAND = 'sudo -u hobo-piwik /usr/bin/piwik-manage.py'
BIJOE_MANAGE_COMMAND = 'sudo -u bijoe /usr/bin/bijoe-manage'
HOBO_MANAGE_COMMAND = 'sudo -u hobo /usr/bin/hobo-manage'

CELERY_SETTINGS = {
    'CELERY_SEND_TASK_ERROR_EMAILS': True,
    'ADMINS': (
        ('Admins', 'root@localhost'),
    ),
}

# run additional settings snippets
ETC_DIR = '/etc/hobo-agent'
execfile('/usr/lib/hobo/debian_config_settings_d.py')
