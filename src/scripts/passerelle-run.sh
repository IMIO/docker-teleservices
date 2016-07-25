#! /bin/sh

test -d /opt/publik/passerelle/ || exit 0
cd /opt/publik/passerelle/
export PASSERELLE_SETTINGS_FILE=/usr/lib/passerelle/debian_config.py
./manage.py collectstatic -l --noinput
./manage.py migrate_schemas --noinput
./manage.py runserver 8011
