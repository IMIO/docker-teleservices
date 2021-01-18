#! /bin/sh

# add entry for LDAP host
if ! grep -q SRV-DC1.tournai.be /etc/hosts
then
    cat >> /etc/hosts << _EOF_
194.78.28.150 SRV-DC1.tournai.be
_EOF_
fi

# install the certificates used on the Active Directory server
cp /opt/publik/hooks/tournaiteleservices/CA-AD-tournai*.crt /usr/local/share/ca-certificates/
update-ca-certificates

# use native authentic translations
rm -f /var/lib/authentic2/locale/fr/LC_MESSAGES/django.mo
