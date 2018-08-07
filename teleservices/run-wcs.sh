#!/bin/bash -ex
service wcs start

tail -f /var/log/syslog
