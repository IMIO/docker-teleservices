#USAGE : docker exec -ti [COMMUNE]teleservices_[COMMUNE]teleservices_1 sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=[COMMUNE]-formulaires.[DOMAIN] /opt/publik/scripts/migration-ts1/export-forms.py [COMMUNE]

import os
import sys
from wcs.formdef import FormDef
for formdef in FormDef.select():
    json_str = formdef.export_to_json()
    folder_store_forms = "/var/tmp/{}".format(sys.argv[1])
    if not os.path.exists(folder_store_forms):
        os.mkdir(folder_store_forms)
    with open ("{}/{}".format(folder_store_forms, formdef.id), 'w') as myfile:
        myfile.write(json_str)
        myfile.close()

