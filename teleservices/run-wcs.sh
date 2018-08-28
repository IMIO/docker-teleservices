#!/bin/bash

/etc/init.d/supervisor start

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DESC="Web Forms Manager"
NAME=wcs
WCSCTL=/usr/bin/wcsctl
DAEMON=/usr/bin/uwsgi
RUN_DIR=/var/run/$NAME
PIDFILE=$RUN_DIR/$NAME.pid
LOG_DIR=/var/log/$NAME
BIND=$RUN_DIR/$NAME.sock
WORKERS=5
TIMEOUT=30

CONFIG_FILE=/etc/wcs/wcs.cfg
WCS_SETTINGS_FILE=/usr/lib/$NAME/debian_config.py
MANAGE_SCRIPT="/usr/bin/$NAME-manage"

USER=$NAME
GROUP=$NAME

# Read configuration variable file if it is present
[ -r /etc/default/$NAME ] && . /etc/default/$NAME

DAEMON_ARGS=${DAEMON_ARGS:-"--pidfile=$PIDFILE
--uid $USER --gid $GROUP
--ini /etc/$NAME/uwsgi.ini"}

# Load the VERBOSE setting and other rcS variables
. /lib/init/vars.sh

# Define LSB log_* functions.
# Depend on lsb-base (>= 3.0-6) to ensure that this file is present.
. /lib/lsb/init-functions

# Create /run directory
if [ ! -d $RUN_DIR ]; then
    install -d -m 775 -o $USER -g $GROUP $RUN_DIR
fi

# environment for wsgi
export WCS_SETTINGS_FILE

$DAEMON $DAEMON_ARGS 
