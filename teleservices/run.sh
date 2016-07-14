#!/bin/bash
rm /var/run/{authentic2-multitenant/authentic2-multitenant,fargo/fargo,combo/combo,nginx,rsyslogd,supervisord,wcs-auquotidien,passerelle/passerelle}.{pid,sock}
/etc/hobo/fix-permissions.sh
service rsyslog start
service combo start
service authentic2-multitenant update
service authentic2-multitenant start
service wcs-au-quotidien start
service passerelle start
service fargo start
service nginx start
service supervisor start
#hobo-manage cook /etc/hobo/recipe.json
/etc/hobo/init.sh
cp -n /etc/authentic2-multitenant/settings.json /var/lib/authentic2-multitenant/tenants/*/

tail -f /var/log/syslog
