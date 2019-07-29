# USAGE : 
# $1 : commune_id (test, demo, local, huy, liege,...)
# $2 : domain (guichet-citoyen.be, example.net, ...)
# $3 : Type Instance light or full (case sensitive)
# $4 : All town's postcodes with a comma as separator (4000,4020,...)

# Use postgresql with wcs
sed -i '/[options] /a postgresql = true' /var/lib/wcs/$1-formulaires.$2/site-options.cfg

# Add resubmit action in workflows
sed -i '/[options] /a workflow-resubmit-action = true' /var/lib/wcs/$1-formulaires.$2/site-options.cfg

# Create categories
sh copy_categories.sh $1 $2

# Create datasources
sh copy_datasources.sh $1 $2

# Create passerelle api user.
sudo -u passerelle /usr/bin/passerelle-manage tenant_command runscript /opt/publik/scripts/build-e-guichet/passerelle/build-api-user.py -d $1-passerelle.$2

# Create passerelle "ts1 datasources connector" with prefilled motivations and destinations terms.
sudo -u passerelle /usr/bin/passerelle-manage tenant_command import_site -d $1-passerelle.$2 /opt/publik/scripts/build-e-guichet/datasources/datasources.json

# Create passerelle "pays" datasource. (To choice country in users' profile).
sudo -u passerelle /usr/bin/passerelle-manage tenant_command import_site -d $1-passerelle.$2 /opt/publik/scripts/build-e-guichet/passerelle/pays.json --import-users

# Add hobo extra params
sudo -u hobo hobo-manage cook /etc/hobo/recipe.json
sed "s~commune~$1~g" hobo/recipe-commune-extra.json > /etc/hobo/recipe-$1-extra.json
test -e /etc/hobo/recipe-$1-extra.json && sudo -u hobo hobo-manage cook /etc/hobo/recipe-$1-extra.json

# Adapt country field in DB to have a list field instead a text field
authentic2-multitenant-manage tenant_command runscript /opt/publik/scripts/build-e-guichet/auth_fedict_var.py -d $1-auth.$2

# Import defaults authentic users
sed -i "s/COMMUNE_ID/$1/g" /opt/publik/scripts/build-e-guichet/import-authentic-user.py
authentic2-multitenant-manage tenant_command runscript /opt/publik/scripts/build-e-guichet/import-authentic-user.py -d $1-auth.$2
sed -i "s/$1/COMMUNE_ID/g" /opt/publik/scripts/build-e-guichet/import-authentic-user.py

# Set permissions
sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/build-e-guichet/import-permissions.py $3

# TODO : voir ce que je peux faire pour les datasources par defaut avec l'url de passerelle hardcodee.
# Import workflows
sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/build-e-guichet/import-workflows.py /opt/publik/scripts/build-e-guichet/workflows/
if [ $3 = "full" ]
    then
    echo "INSTALL WORKFLOWS FOR FULL INSTANCE."
    sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/build-e-guichet/import-workflows.py /opt/publik/scripts/build-e-guichet/workflows/only_full/
fi

# Import forms
if [ $3 = "full" ]
    then
    echo "INSTALL FORMS FOR FULL INSTANCE."
    sed -i "s/<option varname="cp_commune">\[cp_commune\]<\/option>/<option varname="cp_commune">$4<\/option>/g" /opt/publik/scripts/build-e-guichet/forms/only_full/*.wcs
    sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/build-e-guichet/import-forms.py /opt/publik/scripts/build-e-guichet/forms/only_full/
    sed -i "s/<option varname="cp_commune">$4<\/option>/<option varname="cp_commune">\[cp_commune\]<\/option>/g" /opt/publik/scripts/build-e-guichet/forms/only_full/*.wcs
    sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/build-e-guichet/import-forms.py /opt/publik/scripts/build-e-guichet/forms/models/
else
    echo "INSTALL FORMS FOR LIGHT INSTANCE."
    sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/build-e-guichet/import-forms.py /opt/publik/scripts/build-e-guichet/forms/only_light/
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
    sudo -u combo combo-manage tenant_command import_site -d $1.$2 /opt/publik/scripts/build-e-guichet/combo-site/combo-site-structure-full.json
    sed -i "s/$1/COMMUNE/g" combo-site/combo-site-structure-full.json
    sed -i "s/$2/DOMAINE/g" combo-site/combo-site-structure-full.json
else
    sed -i "s/COMMUNE/$1/g" combo-site/combo-site-structure-light.json
    sed -i "s/DOMAINE/$2/g" combo-site/combo-site-structure-light.json
    sudo -u combo combo-manage tenant_command import_site -d $1.$2 /opt/publik/scripts/build-e-guichet/combo-site/combo-site-structure-light.json
    sed -i "s/$1/COMMUNE/g" combo-site/combo-site-structure-light.json
    sed -i "s/$2/DOMAINE/g" combo-site/combo-site-structure-light.json
fi

# Import combo portail agent structure
sed -i "s/COMMUNE/$1/g" combo-site/combo-portail-agent-structure.json
sed -i "s/DOMAINE/$2/g" combo-site/combo-portail-agent-structure.json
sudo -u combo combo-manage tenant_command import_site -d $1-portail-agent.$2 /opt/publik/scripts/build-e-guichet/combo-site/combo-portail-agent-structure.json
sed -i "s/$1/COMMUNE/g" combo-site/combo-portail-agent-structure.json
sed -i "s/$2/DOMAINE/g" combo-site/combo-portail-agent-structure.json

# Create global hobo variables
sudo -u hobo hobo-manage tenant_command runscript -d $1-hobo.$2 /opt/publik/scripts/build-e-guichet/hobo_create_variables.py

cat /etc/combo/settings.py

# Deploy wcs properties : postgresql, smtp_server, homepage_redirect.
sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/build-e-guichet/wcs_config.py $1

echo "sudo -u wcs wcs-manage convert-to-sql --dbname=teleservices_"$1"_wcs --user=teleservices_"$1"_teleservices --password=... --host=database.lan.imio.be" $1"-formulaires.guichet-citoyen.be"

echo "Config mail : mailrelay.imio.be"
