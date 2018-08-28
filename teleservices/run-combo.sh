#!/bin/bash

/etc/init.d/supervisor start

PATH=/sbin:/usr/sbin:/bin:/usr/bin
DESC="Portal Management System"
NAME=combo
DAEMON=/usr/bin/gunicorn
RUN_DIR=/var/run/$NAME
PIDFILE=$RUN_DIR/$NAME.pid
LOG_DIR=/var/log/$NAME
SCRIPTNAME=/etc/init.d/$NAME
BIND=unix:$RUN_DIR/$NAME.sock
WORKERS=5
TIMEOUT=30

export COMBO_SETTINGS_FILE=/usr/lib/$NAME/debian_config.py
MANAGE_SCRIPT="/usr/bin/$NAME-manage"

USER=$NAME
GROUP=$NAME

# Exit if the package is not installed
[ -x $MANAGE_SCRIPT ] || exit 0

# Read configuration variable file if it is present
[ -r /etc/default/$NAME ] && . /etc/default/$NAME

DAEMON_ARGS=${DAEMON_ARGS:-"--pid $PIDFILE \
--user $USER --group $GROUP \
--access-logfile $LOG_DIR/gunicorn-access.log \
--log-file $LOG_DIR/gunicorn-error.log \
--bind=$BIND  \
--workers=$WORKERS \
--worker-class=sync \
--timeout=$TIMEOUT \
--name $NAME \
$NAME.wsgi:application"}

$DAEMON $DAEMON_ARGS
