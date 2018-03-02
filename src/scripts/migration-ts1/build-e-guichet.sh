# USAGE : 
# $1 : commune_id (test, demo, local, huy, liege,...)
# $2 : domain (guichet-citoyen.be, example.net, ...)
# $3 : Type Instance light or full (case sensitive)

# Use postgresql with wcs
sed -i '/[options] /a postgresql = true' /var/lib/wcs/$1-formulaires.$2/site-options.cfg

# Create categories
sh copy_categories.sh $1 $2

# Create datasources
sh copy_datasources.sh $1 $2

# Import wcs user to limit site permissions
# sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/migration-ts1/import-wcs-user.py

# Import defaults authentic users
sed -i "s/COMMUNE_ID/$1/g" /opt/publik/scripts/migration-ts1/import-authentic-user.py
authentic2-multitenant-manage tenant_command runscript /opt/publik/scripts/migration-ts1/import-authentic-user.py -d $1-auth.$2
sed -i "s/$1/COMMUNE_ID/g" /opt/publik/scripts/migration-ts1/import-authentic-user.py

# Set permissions
sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/migration-ts1/import-permissions.py $3

# Create passerelle "ts1 datasources connector" with prefilled motivations and destinations terms.
sudo -u passerelle /usr/bin/passerelle-manage tenant_command import_site -d $1-passerelle.$2 /opt/publik/scripts/migration-ts1/datasources/datasources.json

# Create passerelle api user.
sudo -u passerelle /usr/bin/passerelle-manage tenant_command runscript /opt/publik/scripts/migration-ts1/passerelle/build-api-user.py -d $1-passerelle.$2

# Create passerelle "pays" datasource. (To choice country in users' profile).
sudo -u passerelle /usr/bin/passerelle-manage tenant_command import_site -d $1-passerelle.$2 /opt/publik/scripts/migration-ts1/passerelle/pays.json

# TODO : voir ce que je peux faire pour les datasources par defaut avec l'url de passerelle hardcodee.

# Import workflows
sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/migration-ts1/import-workflows.py /opt/publik/scripts/migration-ts1/workflows/
if [ $3 = "full" ]
    then
    echo "INSTALL WORKFLOWS FOR FULL INSTANCE."
    sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/migration-ts1/import-workflows.py /opt/publik/scripts/migration-ts1/workflows/only_full/
fi

# Import forms
if [ $3 = "full" ]
    then
    echo "INSTALL FORMS FOR FULL INSTANCE."
    sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/migration-ts1/import-ts1-forms.py /opt/publik/scripts/migration-ts1/forms/
    sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/migration-ts1/import-ts1-forms.py /opt/publik/scripts/migration-ts1/forms/only_full/
else
    echo "INSTALL FORMS FOR LIGHT INSTANCE."
    sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/migration-ts1/import-ts1-forms.py /opt/publik/scripts/migration-ts1/forms/only_light/
fi

# Create regie
sudo -u combo combo-manage tenant_command runscript -d $1.$2 lingo_create_regie.py
# Puppet deploy search for : create_regie.py.erb
if [ -f /var/lib/combo/create_regie.py ]
    then
sudo -u combo combo-manage tenant_command import_site -d $1-portail-agent.$2 /var/lib/combo/create_regie.py
fi

# Import combo site structure
if [ $3 = "full" ]
    then
    sed -i "s/COMMUNE/$1/g" combo-site/combo-site-structure-full.json
    sed -i "s/DOMAINE/$2/g" combo-site/combo-site-structure-full.json
    sudo -u combo combo-manage tenant_command import_site -d $1.$2 /opt/publik/scripts/migration-ts1/combo-site/combo-site-structure-full.json
    sed -i "s/$1/COMMUNE/g" combo-site/combo-site-structure-full.json
    sed -i "s/$2/DOMAINE/g" combo-site/combo-site-structure-full.json
else
    sed -i "s/COMMUNE/$1/g" combo-site/combo-site-structure-light.json
    sed -i "s/DOMAINE/$2/g" combo-site/combo-site-structure-light.json
    sudo -u combo combo-manage tenant_command import_site -d $1.$2 /opt/publik/scripts/migration-ts1/combo-site/combo-site-structure-light.json
    sed -i "s/$1/COMMUNE/g" combo-site/combo-site-structure-light.json
    sed -i "s/$2/DOMAINE/g" combo-site/combo-site-structure-light.json
fi

sed -i "s/COMMUNE/$1/g" combo-site/combo-portail-agent-structure.json
sed -i "s/DOMAINE/$2/g" combo-site/combo-portail-agent-structure.json
sudo -u combo combo-manage tenant_command import_site -d $1-portail-agent.$2 /opt/publik/scripts/migration-ts1/combo-site/combo-portail-agent-structure.json
sed -i "s/$1/COMMUNE/g" combo-site/combo-portail-agent-structure.json
sed -i "s/$2/DOMAINE/g" combo-site/combo-portail-agent-structure.json

# Create global hobo variables
sudo -u hobo hobo-manage tenant_command runscript -d $1-hobo.$2 /opt/publik/scripts/migration-ts1/hobo_create_variables.py

# Add hobo extra params
sudo -u hobo hobo-manage cook /etc/hobo/recipe.json
sed "s~commune~$1~g" hobo/recipe-commune-extra.json > /etc/hobo/recipe-$1-extra.json
test -e /etc/hobo/recipe-$1-extra.json && sudo -u hobo hobo-manage cook /etc/hobo/recipe-$1-extra.json

cat /etc/combo/settings.py
echo "Config mail : mailrelay.imio.be"
