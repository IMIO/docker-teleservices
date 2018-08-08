#!/bin/bash
PATH=/sbin:/usr/sbin:/bin:/usr/bin
DESC=authentic2
NAME=authentic2-multitenant
DAEMON=/usr/bin/gunicorn
PID_DIR=/var/run/$NAME
CACHE_DIR=/var/cache/$NAME
LOG_DIR=/var/log/$NAME
PIDFILE=$PID_DIR/$NAME.pid
SCRIPTNAME=/etc/init.d/$NAME
BIND=unix:$PID_DIR/$NAME.sock
WORKERS=4

export AUTHENTIC2_SETTINGS_FILE=/usr/lib/$NAME/debian_config.py
MANAGE_SCRIPT="/usr/bin/$NAME-manage"

USER=authentic-multitenant
GROUP=authentic-multitenant

/usr/bin/gunicorn --pid $PIDFILE \
--user $USER --group $GROUP \
--access-logfile $LOG_DIR/gunicorn-access.log \
--log-file $LOG_DIR/gunicorn-error.log \
--bind=$BIND \
--workers=$WORKERS \
--worker-class=sync \
--timeout=60 \
authentic2.wsgi:application
