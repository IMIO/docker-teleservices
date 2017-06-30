import os
import sys
from wcs.formdef import FormDef
lst_formdef_ids = []
lst_formdef_names = []
conv = lambda x: int(x)
for formdef in FormDef.select():
    lst_formdef_names.append(formdef.name)
    lst_formdef_ids.append(formdef.id)
# default folder path : # "/opt/publik/scripts/migration-ts1/forms/"
folder_path = sys.argv[1]
for fichier in os.listdir(folder_path):
    if fichier[-4:] == ".wcs":
        fd = open("{}{}".format(folder_path, fichier))
        print fichier
        formdef = FormDef.import_from_xml(fd, charset='utf-8', include_id=False)
        print formdef.name
        if formdef.name not in lst_formdef_names:
            formdef.disabled = False
            if formdef.category.id == "99":
                try:
                    with open("/tmp/tmp_uuid_agent_traitant_pop.txt", 'r') as file_at:
                        uuid_at = file_at.read()
                        formdef.workflow_roles = {'_receiver':uuid_at}
                except:
                        uuid_at = 12
                        formdef.workflow_roles = {'_receiver':uuid_at}
            else:
                try:
                    with open("/tmp/tmp_uuid_agent_traitant_trav.txt", 'r') as file_at:
                        uuid_at = file_at.read()
                        formdef.workflow_roles = {'_receiver':uuid_at}
                except:
                        uuid_at = 13
                        formdef.workflow_roles = {'_receiver':uuid_at}
            try:
                if len(lst_formdef_ids) < 1:
                    new_id = 1
                else:
                    new_id = int(sorted(lst_formdef_ids, key=conv)[-1]) + 1
                lst_formdef_ids.append(new_id)
                formdef.id = new_id
                formdef.store()
            except:
                print "import error : " + formdef.id

