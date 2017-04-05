# SAMPLE : sh copy_categories.sh lalouviere lescommunes.be
if ! [ -d /var/lib/wcs-au-quotidien/$1-formulaires.$2/datasrouces ]
then
    (mkdir /var/lib/wcs-au-quotidien/$1-formulaires.$2/datasources)
fi

sed "s~http://local-passerelle.example.net~https://$1-passerelle.$2~g" datasources/98 > /var/lib/wcs-au-quotidien/$1-formulaires.$2/datasources/98
sed "s~http://local-passerelle.example.net~https://$1-passerelle.$2~g" datasources/99 > /var/lib/wcs-au-quotidien/$1-formulaires.$2/datasources/99
