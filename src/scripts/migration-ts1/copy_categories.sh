# SAMPLE : sh copy_categories.sh lalouviere lescommunes.be
if ! [ -d /var/lib/wcs-au-quotidien/$1-formulaires.$2/categories ]
then
    (mkdir /var/lib/wcs-au-quotidien/$1-formulaires.$2/categories)
fi

cp categories/* /var/lib/wcs-au-quotidien/$1-formulaires.$2/categories