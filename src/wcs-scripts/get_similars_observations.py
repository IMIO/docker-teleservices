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

result = ''

def get_similars_observations_count(data):
    coords = close_demands.get_coords(data)
    result = "0"
    if coords:
        lst_similar_forms = list(close_demands.get_close_demands(form_objects.formdef, coords, vars()))
        result = str(len(lst_similar_forms))
    return result

#form_status : contient le status courant de la demande.
def get_similars_observations_mails(data):
    coords = close_demands.get_coords(data)
    lst_mails = []
    result = ''
    if coords:
        lst_similar_forms = list(close_demands.get_close_demands(form_objects.formdef, coords, vars()))
        if len(lst_similar_forms) > 0:
            formdef = lst_similar_forms[0].formdef
            formdatas = formdef.data_class().select(lambda x: x.id_display!=form_number)
            for formdata in formdatas:
                for field in formdef.get_all_fields():
                    # possiblement, faire evoluer le wf de la demande courante jusqu'au statut dans lequel est la 1ere demande? Sauf si cette demande est deja plus loin dans le wf?
                    if field.varname is not None and  "mail_for_similar_observation" in field.varname:
                        lst_mails.append(formdata.get_field_view_value(field))
        result = ','.join(lst_mails)
    return result

if args[0] == "mail":
    result = get_similars_observations_mails(vars())
if args[0] == "count":
    result = get_similars_observations_count(vars())
