#!/bin/bash -ex
service bijoe start

tail -f /var/log/syslog
