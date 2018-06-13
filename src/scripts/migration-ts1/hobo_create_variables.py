#usage : sudo -u hobo hobo-manage tenant_command runscript -d demo-hobo.guichet-citoyen.be /opt/publik/scripts/migration-ts1/hobo_create_variables.py
from hobo.environment.models import Variable
Variable(name='commune_name', label='Nom de la commune', value='Ma Commune').save()
Variable(name='commune_slug', label='Nom de la commune sans accent, sans espace (mettre des tirets), en minuscule.', value='ma-commune').save()
Variable(name='commune_cp', label='Code postal de la commune', value='1111').save()
Variable(name='commune_rue', label='Rue et n° de la commune', value='1, Rue de ma Commune').save()
Variable(name='commune_site', label='Site Internet de la commune', value='1, Rue de ma Commune').save()
