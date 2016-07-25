#! /bin/sh

test -d /opt/publik/combo/ || exit 0
cd /opt/publik/combo/

export COMBO_SETTINGS_FILE=/usr/lib/combo/debian_config.py
./manage.py collectstatic -l --noinput
./manage.py migrate_schemas --noinput
./manage.py runserver 8010
