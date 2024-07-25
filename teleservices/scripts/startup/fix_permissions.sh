#!/bin/bash

prefix="✨ check_permissions.sh ·"

echo -n "$prefix updating some Entr'Ouvert services folders user:group via chown..."
chown authentic-multitenant:authentic-multitenant /var/lib/authentic2-multitenant/tenants -R &&
chown hobo:hobo /var/lib/hobo/tenants -R &&
chown bijoe:bijoe /var/lib/bijoe/tenants -R &&
chown chrono:chrono /var/lib/chrono/tenants -R &&
chown combo:combo /var/lib/combo/tenants -R &&
chown passerelle:passerelle /var/lib/passerelle/tenants -R &&
chown wcs:wcs /var/lib/wcs -R &&
echo " done! ✅"

echo -n "$prefix verifying uploads & attachments permission folders..."
[ -d /var/lib/wcs/tenants/*/attachments ] && (chown -R wcs:wcs /var/lib/wcs/tenants/*/attachments/ && echo -n " attachments done! ✅..." || echo -n " attachments failed! ❌...") || echo -n " attachments skipped! 🚫... "
[ -d /var/lib/wcs/tenants/*/uploads ] && (chown -R wcs:wcs var/lib/wcs/tenants/*/uploads/ && echo " uploads done! ✅" || echo "uploads failed! ❌") || echo " uploads skipped! 🚫"
