#USAGE : docker exec -ti [COMMUNE]teleservices_[COMMUNE]teleservices_1 sudo -u  wcs-au-quotidien wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=[COMMUNE]-formulaires.[DOMAIN] /opt/publik/scripts/migration-ts1/export-forms.py [COMMUNE]

import os
import sys
import xml.etree.ElementTree as ET
from wcs.workflows import Workflow
from qommon import misc

for wf in Workflow.select():
    xml = wf.export_to_xml(include_id=True)
    misc.indent_xml(xml)
    xml_str = ET.tostring(xml)
    folder_store_forms = "/var/lib/wcs/xml_wf_{}".format(sys.argv[1])
    if not os.path.exists(folder_store_forms):
        os.mkdir(folder_store_forms)
    with open ("{}/{}.wcs".format(folder_store_forms, formdef.internal_identifier), 'w+') as myfile:
        myfile.write(xml_str)
