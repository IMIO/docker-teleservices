# -*- coding: utf-8 -*-
# sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/build-e-guichet/wcs_config.py $1

import os
import sys
from quixote import get_publisher

pub = get_publisher()
pub.cfg['misc']['homepage-redirect-url'] = 'https://{0}.guichet-citoyen.be/demarches/'.format(sys.argv[1])

pub.cfg['postgresql']['database'] = 'teleservices_{0}_wcs'.format(sys.argv[1])
pub.cfg['postgresql']['user'] = 'teleservices_{0}_teleservices'.format(sys.argv[1])
pub.cfg['postgresql']['host'] = 'database.lan.imio.be'
pub.cfg['postgresql']['port'] = '5432'
with open('/etc/combo/settings.py') as f:
    for line in f:
        if "DATABASES['default']['PASSWORD']" in line:
            password = line.split(' = ')[1].translate(None, "'")
pub.cfg['postgresql']['password'] = password
pub.cfg['emails']['smtp_server'] = 'mailrelay.imio.be'
pub.write_cfg()
