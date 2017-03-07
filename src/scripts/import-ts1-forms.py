import os
from wcs.formdef import FormDef

path = "/opt/publik/scripts/forms-samples/"
dirs = os.listdir(path)
# print existing forms.
for formdef in FormDef.select():
    print formdef

# add new forms in e-guichet instance.
for currfile in dirs:
    print "{}{}".format(path, currfile)
    fd = open("{}{}".format(path, currfile))
    formdef = FormDef.import_from_xml(fd, charset=None, include_id=False)
    formdef.store()

