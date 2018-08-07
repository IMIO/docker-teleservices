#!/bin/bash -ex
service passerelle start
COPY run-passerelle.sh /

tail -f /var/log/syslog
