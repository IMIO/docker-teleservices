# authentic2-multitenant-manage tenant_command runscript /opt/publik/scripts/build-e-guichet/auth_var.py -d $1-auth.$2
from authentic2.models import Attribute
Attribute.objects.filter(name = 'country').update(kind='country')
