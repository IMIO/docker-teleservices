# SAMPLE : sh copy_categories.sh lalouviere lescommunes.be
if ! [ -d /var/lib/wcs/$1-formulaires.$2/datasources ]
then
    (mkdir /var/lib/wcs/$1-formulaires.$2/datasources && chown wcs:wcs /var/lib/wcs/$1-formulaires.$2/datasources -Rf)
fi

sed "s~http://local-passerelle.example.net~https://$1-passerelle.$2~g" datasources/98 > /var/lib/wcs/$1-formulaires.$2/datasources/98
sed "s~http://local-passerelle.example.net~https://$1-passerelle.$2~g" datasources/99 > /var/lib/wcs/$1-formulaires.$2/datasources/99
sed "s~http://local-passerelle.example.net~https://$1-passerelle.$2~g" datasources/100 > /var/lib/wcs/$1-formulaires.$2/datasources/100
sed "s~http://local-passerelle.example.net~https://$1-passerelle.$2~g" datasources/101 > /var/lib/wcs/$1-formulaires.$2/datasources/101
sed "s~http://local-passerelle.example.net~https://$1-passerelle.$2~g" datasources/102 > /var/lib/wcs/$1-formulaires.$2/datasources/102
sed "s~http://local-passerelle.example.net~https://$1-passerelle.$2~g" datasources/103 > /var/lib/wcs/$1-formulaires.$2/datasources/103
sed "s~http://local-passerelle.example.net~https://$1-passerelle.$2~g" datasources/104 > /var/lib/wcs/$1-formulaires.$2/datasources/104
sed "s~http://local-passerelle.example.net~https://$1-passerelle.$2~g" datasources/105 > /var/lib/wcs/$1-formulaires.$2/datasources/105
sed "s~http://local-passerelle.example.net~https://$1-passerelle.$2~g" datasources/106 > /var/lib/wcs/$1-formulaires.$2/datasources/106
sed "s~http://local-passerelle.example.net~https://$1-passerelle.$2~g" datasources/108 > /var/lib/wcs/$1-formulaires.$2/datasources/108
sed "s~http://local-passerelle.example.net~https://$1-passerelle.$2~g" datasources/109 > /var/lib/wcs/$1-formulaires.$2/datasources/109
sed "s~http://local-passerelle.example.net~https://$1-passerelle.$2~g" datasources/110 > /var/lib/wcs/$1-formulaires.$2/datasources/110
sed "s~http://local-passerelle.example.net~https://$1-passerelle.$2~g" datasources/111 > /var/lib/wcs/$1-formulaires.$2/datasources/111
