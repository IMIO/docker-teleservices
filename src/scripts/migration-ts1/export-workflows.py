#USAGE : docker exec -ti [COMMUNE]teleservices_[COMMUNE]teleservices_1 sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=[COMMUNE]-formulaires.[DOMAIN] /opt/publik/scripts/migration-ts1/export-workflows.py [COMMUNE]

import os
import sys
import xml.etree.ElementTree as ET
from django.template.defaultfilters import slugify
from wcs.workflows import Workflow
from qommon import misc

for wf in Workflow.select():
    xml = wf.export_to_xml(include_id=True)
    misc.indent_xml(xml)
    xml_str = ET.tostring(xml)
    folder_store_wf = "/var/lib/wcs/xml_wf_{}".format(sys.argv[1])
    if not os.path.exists(folder_store_wf):
        os.mkdir(folder_store_wf)
    with open ("{}/{}.wcs".format(folder_store_wf, slugify(wf.name)), 'w+') as myfile:
        myfile.write(xml_str)
