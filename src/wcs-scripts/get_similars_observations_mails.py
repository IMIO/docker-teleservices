# Scripts for map statement management:
# close_demands.py  
# has_close_demands.py  
# similar_list.py  
# similar_map.py

import os
import sys

if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.dirname(__file__))

import close_demands
coords = close_demands.get_coords(vars())
lst_mails = []
if coords:
    lst_similar_forms = list(close_demands.get_close_demands(form_objects.formdef, coords, vars()))
    if len(lst_similar_forms) > 0:
        formdef = lst_similar_forms[0].formdef
        formdatas = formdef.data_class().select()
        for formdata in formdatas:
            for field in formdef.get_all_fields():
                if field.varname is not None and  "mail_for_similar_observation" in field.varname:
                    lst_mails.append(formdata.get_field_view_value(field))
    result = ','.join(lst_mails)
else:
    result = ''

