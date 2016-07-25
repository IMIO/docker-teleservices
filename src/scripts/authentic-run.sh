#! /bin/sh

test -d /opt/publik/authentic/ || exit 0
cd /opt/publik/authentic/

export AUTHENTIC2_SETTINGS_FILE=/usr/lib/authentic2-multitenant/debian_config.py
./authentic2-ctl collectstatic -l --noinput
./authentic2-ctl migrate_schemas --noinput
./authentic2-ctl runserver 8012
