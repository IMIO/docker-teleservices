#!/bin/bash
# Sample : Loop accross dockers instances and add defaults roles, users and permissions.
set +x
for commune in 'silly' 'olln' 'lierneux' 'huy' 'ecaussinnes' 'honnelles' 'courcelles' 'boussu'
    do
            docker exec -ti $commune"teleservices_"$commune"teleservices_1" sed -i "s/COMMUNE_ID/"$commune"/g" /opt/publik/scripts/migration-ts1/import-authentic-user.py
            docker exec -ti $commune"teleservices_"$commune"teleservices_1" authentic2-multitenant-manage tenant_command runscript /opt/publik/scripts/migration-ts1/import-authentic-user.py -d $commune"-auth.guichet-citoyen.be"
            docker exec -ti $commune"teleservices_"$commune"teleservices_1" sed -i "s/"$commune"/COMMUNE_ID/g" /opt/publik/scripts/migration-ts1/import-authentic-user.py


            docker exec -ti $commune"teleservices_"$commune"teleservices_1" sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$commune"-formulaires.guichet-citoyen.be" /opt/publik/scripts/migration-ts1/import-permissions.py full
    done

