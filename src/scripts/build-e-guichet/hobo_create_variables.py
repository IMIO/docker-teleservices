#usage : sudo -u hobo hobo-manage tenant_command runscript -d demo-hobo.guichet-citoyen.be /opt/publik/scripts/build-e-guichet/hobo_create_variables.py
from hobo.environment.models import Variable
Variable(name='commune_name', label='Nom de la commune', value='Ma Commune').save()
Variable(name='commune_slug', label='Nom de la commune sans accent, sans espace (mettre des tirets), en minuscule.', value='ma-commune').save()
Variable(name='commune_cp', label='Code postal/postaux de la commune', value='1111').save()
Variable(name='administration_adresse', label="Adresse complète de l'administration", value="1, Place de l'administration - 1111 Ma Commune").save()
Variable(name='administration_site', label='Site Internet de la commune', value='https://www.ma-commune.be').save()
Variable(name='global_title', label='Intitulé de l\'instance et mails', value='Commune - Guichet en ligne').save()
