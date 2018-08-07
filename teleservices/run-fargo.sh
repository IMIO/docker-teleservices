#!/bin/bash
PATH=/sbin:/usr/sbin:/bin:/usr/bin
DESC="Document Box"
NAME=fargo
DAEMON=/usr/bin/gunicorn
RUN_DIR=/var/run/$NAME
PIDFILE=$RUN_DIR/$NAME.pid
LOG_DIR=/var/log/$NAME
SCRIPTNAME=/etc/init.d/$NAME
BIND=unix:$RUN_DIR/$NAME.sock
WORKERS=5
TIMEOUT=30

FARGO_SETTINGS_FILE=/usr/lib/$NAME/debian_config.py
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

# Load the VERBOSE setting and other rcS variables
. /lib/init/vars.sh

# Define LSB log_* functions.
# Depend on lsb-base (>= 3.0-6) to ensure that this file is present.
. /lib/lsb/init-functions

# Create /run directory
if [ ! -d $RUN_DIR ]; then
    install -d -m 755 -o $USER -g $GROUP $RUN_DIR
fi

# environment for wsgi
export FARGO_SETTINGS_FILE

$DAEMON $DAEMON_ARGS
