#! /bin/sh

# add entry for LDAP host
if ! grep -q SRV-DC1.tournai.be /etc/hosts
then
    cat >> /etc/hosts << _EOF_
194.78.28.150 SRV-DC1.tournai.be
_EOF_
fi
