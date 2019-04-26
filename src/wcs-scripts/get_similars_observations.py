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
list_sous_domaines = ['var_sous_domaine_proprete',
        'var_sous_domaine_avaloir',
        'var_sous_domaine_voirie',
        'var_sous_domaine_graffiti',
        'var_sous_domaine_espace_vert',
        'var_sous_domaine_signalisation',
        'var_sous_domaine_mobilier_urbain',
        'var_sous_domaine_voirie'
        ]


def get_similars_observations_count(data):
    coords = close_demands.get_coords(data)
    result = 0
    if coords:
        for item in close_demands.get_close_demands(form_objects.formdef, coords, data):
            structured_item =  item.get_as_dict()
            if structured_item['var_incident'] == form_var_incident:
                for sous_domaine in list_sous_domaines:
                    if structured_item.has_key(sous_domaine):
                        if structured_item[sous_domaine] is not None and structured_item[sous_domaine] == data.get('form_{}'.format(sous_domaine)):
                            result = result + 1
    return str(result)

#form_status : contient le status courant de la demande.
def get_similars_observations_mails(data):
    coords = close_demands.get_coords(data)
    lst_mails = []
    result = ''
    if coords:
        for item in close_demands.get_close_demands(form_objects.formdef, coords, data):
            structured_item =  item.get_as_dict()
            if structured_item['var_incident'] == form_var_incident:
                for sous_domaine in list_sous_domaines:
                    if structured_item.has_key(sous_domaine):
                        if structured_item[sous_domaine] is not None and structured_item[sous_domaine] == data.get('form_{}'.format(sous_domaine)):
                            if structured_item.has_key('var_mail_for_similar_observation') and \
                                    structured_item['var_mail_for_similar_observation'] is not None:
                                lst_mails.append(formdata.get_field_view_value(field))
        result = ','.join(lst_mails)
    return result

if args[0] == "mail":
    result = get_similars_observations_mails(vars())
if args[0] == "count":
    result = get_similars_observations_count(vars())
