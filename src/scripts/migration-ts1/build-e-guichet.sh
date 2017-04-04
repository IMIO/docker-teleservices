# $1 : commune_id (test, local, huy, liege,...)
# $2 : domain (guichet-citoyen.be, example.net, ...)

# Create categories
run sh copy_categories.sh $1 $2

# Import wcs user to limit site permissions
sudo -u  wcs-au-quotidien wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/migration-ts1/import-wcs-user.py

# Import defaults authentic users
authentic2-multitenant-manage tenant_command runscript /opt/publik/scripts/migration-ts1/import-authentic-user.py -d $1-auth.$2

# Set permissions
sudo -u  wcs-au-quotidien wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/migration-ts1/import-permissions.py

# Create passerelle "ts1 datasources connector" with prefilled motivations and destinations terms.
sudo -u passerelle /usr/bin/passerelle-manage tenant_command import_site -d $1-passerelle.$2 /opt/publik/scripts/migration-ts1/datasources/datasources.json

# TODO : voir ce que je peux faire pour les datasources par defaut avec l'url de passerelle hardcodee.
# TO : voir ce que je peux faire pour la datasource de la liste des pays... autant qu'elle soit dedans ;-).

# Import workflows
sudo -u  wcs-au-quotidien wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/migration-ts1/import-workflows.py /opt/publik/scripts/migration-ts1/workflows/

# Import forms
sudo -u  wcs-au-quotidien wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/migration-ts1/import-forms.py /opt/publik/scripts/migration-ts1/forms/

# Import combo site structure
combo-manage tenant_command import_site -d $1.$2 /opt/publik/scripts/migration-ts1/combo-site/combo-site-structure.json

