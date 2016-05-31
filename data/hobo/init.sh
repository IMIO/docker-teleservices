#!/bin/sh
set +ex
apt-get install  --force-yes -y sudo
sudo -u authentic-multitenant authentic2-multitenant-manage hobo_deploy --ignore-timestamp http://local-auth.example.net/ /etc/hobo/hobo.json
sudo -u combo combo-manage hobo_deploy --ignore-timestamp http://local.example.net/ /etc/hobo/hobo.json
sudo -u combo combo-manage hobo_deploy --ignore-timestamp http://local-portail-agent.example.net/ /etc/hobo/hobo.json
sudo -u fargo fargo-manage  hobo_deploy --ignore-timestamp http://local-documents.example.net/ /etc/hobo/hobo.json 
sudo -u passerelle passerelle-manage  hobo_deploy --ignore-timestamp http://local-passerelle.example.net/ /etc/hobo/hobo.json 
sudo -u wcs-au-quotidien wcsctl -f /etc/wcs/wcs-au-quotidien.cfg hobo_deploy --ignore-timestamp http://local-formulaires.example.net/ /etc/hobo/hobo.json
sudo -u authentic-multitenant authentic2-multitenant-manage hobo_deploy --ignore-timestamp http://local-auth.example.net/ /etc/hobo/hobo.json
if ! grep postgresql /var/lib/wcs-au-quotidien/local-formulaires.example.net/site-options.cfg;
then
    echo "postgresql = true" >> /var/lib/wcs-au-quotidien/local-formulaires.example.net/site-options.cfg
fi
for rsrc in static templates
do
    rep="/var/lib/combo/tenants/local-portail-agent.example.net/$rsrc"
    test -L $rep || $(rm -rf $rep ; ln -s /usr/share/combo/themes/gadjo/$rsrc $rep)
done
echo "You can now set the postgresql config for wcs in http://local.example.net"
echo "dbname: wcs"
echo "dbuser: postgres"
echo "dbpassword: password"
echo "dbhost: database"
echo "dbport: 5432"
