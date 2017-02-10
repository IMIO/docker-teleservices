#!/bin/bash
rm /var/run/{authentic2-multitenant/authentic2-multitenant,fargo/fargo,hobo/hobo,combo/combo,nginx,rsyslogd,supervisord,wcs-auquotidien,passerelle/passerelle,bijoe/bijoe}.{pid,sock}
/etc/hobo/fix-permissions.sh

python /var/lib/authentic2/locale/fr/LC_MESSAGES/mail-translation.py

# install link to wcs external scripts
test -e /var/lib/wcs-au-quotidien/scripts || ln -s /opt/publik/wcs-scripts /var/lib/wcs-au-quotidien/scripts

HOSTNAME=$(hostname)
test -f /opt/publik/hooks/$HOSTNAME/run-hook.sh && /opt/publik/hooks/$HOSTNAME/run-hook.sh

service rsyslog start

if [ x$1 != xfromgit ] || [ ! -d /opt/publik/combo ]
then
	service combo start
fi

if [ x$1 != xfromgit ] || [ ! -d /opt/publik/authentic ]
then
	service authentic2-multitenant update
	service authentic2-multitenant start
fi

if [ x$1 != xfromgit ] || [ ! -d /opt/publik/wcs ]
then
	service wcs-au-quotidien start
fi

if [ x$1 != xfromgit ] || [ ! -d /opt/publik/passerelle ]
then
	service passerelle start
fi

service hobo start
service fargo start
service bijoe start
service nginx start
service supervisor start
sudo -u hobo hobo-manage cook /etc/hobo/recipe.json
test -e /etc/hobo/recipe*extra.json && sudo -u hobo hobo-manage cook /etc/hobo/recipe*extra.json
test -e /var/lib/authentic2-multitenant/tenants/*/settings.json || ln -s /etc/authentic2-multitenant/settings.json /var/lib/authentic2-multitenant/tenants/*/

if [ x$1 = xfromgit ]
then
	/opt/publik/scripts/init-dev.sh
	screen -d -m -c /opt/publik/screenrc
fi

tail -f /var/log/syslog
