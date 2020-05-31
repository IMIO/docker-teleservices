# usage : sudo -u hobo hobo-manage tenant_command runscript -d demo-hobo.guichet-citoyen.be /opt/publik/scripts/build-e-guichet/hobo_create_variables.py
from hobo.environment.models import Variable
Variable(name='commune_name', label='Nom de la commune', value='Ma Commune').save()
Variable(name='commune_slug', label='Nom de la commune sans accent, sans espace (mettre des tirets), en minuscule.', value='ma-commune').save()
Variable(name='commune_cp', label='Code postal/postaux de la commune', value='1111').save()
Variable(name='administration_adresse', label="Adresse complète de l'administration", value="1, Place de l'administration - 1111 Ma Commune").save()
Variable(name='administration_site', label='Site Internet de la commune', value='https://www.ma-commune.be').save()
Variable(name='global_title', label='Intitulé de l\'instance et mails', value='Commune - Guichet en ligne').save()
variables = Variable.objects
variables.filter(name='default_from_email').update(value='e-guichet@imio.be')

#dic_default_from_email = ''
#for variable in variables.values():
#    if variable.get('name') == 'default_from_email':
#        dic_default_from_email = variable
#obj, created = variables.update_or_create(
#    name='default_from_email', value='no-reply@imio.be',
#    defaults=dic_default_from_email,
#)

