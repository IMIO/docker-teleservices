#! /bin/sh
# To get extra.js in Backoffice.
if [ -d "/var/lib/wcs/namur-formulaires.lescommunes.be" ]; then
    cp site-options-preprod.cfg /var/lib/wcs/namur-formulaires.lescommunes.be/site-options.cfg
else
    cp site-option-prod.cfg /var/lib/wcs/namur-formulaires.guichet-citoyen.be/site-options.cfg
fi
