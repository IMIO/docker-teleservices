#!/bin/bash
rm /var/run/{authentic2-multitenant/authentic2-multitenant,fargo/fargo,combo/combo,nginx,rsyslogd,supervisord,wcs-auquotidien,passerelle/passerelle}.{pid,sock}
/etc/hobo/fix-permissions.sh
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

service fargo start
service nginx start
service supervisor start
#hobo-manage cook /etc/hobo/recipe.json
/etc/hobo/init.sh
test -e /var/lib/authentic2-multitenant/tenants/*/settings.json || ln -s /etc/authentic2-multitenant/settings.json /var/lib/authentic2-multitenant/tenants/*/

if [ x$1 = xfromgit ]
then
	/opt/publik/scripts/init-dev.sh
	screen -d -m -c /opt/publik/screenrc
fi

tail -f /var/log/syslog
