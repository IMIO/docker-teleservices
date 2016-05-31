#!/bin/sh
set +ex
if ! grep theme_skeleton_url /var/lib/wcs-au-quotidien/local-formulaires.example.net/site-options.cfg;
then
     echo "Don't forget to add 'theme_skeleton_url = http://local.example.net/__skeleton__/' in /var/lib/wcs-au-quotidien/local-formulaires.example.net/site-options.cfg in option section."
fi
# echo '{ "THEME_SKELETON_URL": "https://local.example.net/__skeleton__/" }' > /var/lib/authentic2-multitenant/tenants/local-auth.example.net/settings.json

for base_dir in /var/lib/combo/tenants/local.example.net /var/lib/authentic2-multitenant/tenants/local-auth.example.net /var/lib/passerelle/tenants/local-passerelle.example.net
do
    ln -s /usr/share/publik/themes/publik-base $base_dir/theme
    for directory in static templates;
    do
        if [ -d $base_dir/$directory ]; then
            rm -rf $base_dir/$directory
            ln -s /usr/share/publik/themes/publik-base/$directory $base_dir/$directory
        fi
    done
done
