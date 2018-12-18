# SAMPLE : sh copy_categories.sh lalouviere lescommunes.be
if ! [ -d /var/lib/wcs/$1-formulaires.$2/categories ]
then
    (mkdir /var/lib/wcs/$1-formulaires.$2/categories && chown wcs:wcs /var/lib/wcs/$1-formulaires.$2/categories -Rf)
fi

cp categories/* /var/lib/wcs/$1-formulaires.$2/categories
