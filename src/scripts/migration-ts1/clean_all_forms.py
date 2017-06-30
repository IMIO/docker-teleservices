# Clean all forms in Treatment!! (Not in kart)
from wcs.formdef import FormDef
for formdef in FormDef.select():
        formdef.data_class().wipe()
