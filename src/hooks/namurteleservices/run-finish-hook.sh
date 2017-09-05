#! /bin/sh
# To get extra.js in Backoffice.
if [ -d "/var/lib/wcs-au-quotidien/namur-formulaires.lescommunes.be" ]; then
    cp site-option.cfg /var/lib/wcs-au-quotidien/namur-formulaires.lescommunes.be
else
    cp site-option.cfg /var/lib/wcs-au-quotidien/namur-formulaires.guichet-citoyen.be
fi
