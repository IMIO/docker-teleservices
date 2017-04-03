if ! [ -d /var/lib/wcs-au-quotidien/local-formulaires.example.net/categories ]
then
    (mkdir /var/lib/wcs-au-quotidien/local-formulaires.example.net/categories)
fi

cp categories/* /var/lib/wcs-au-quotidien/local-formulaires.example.net/categories
