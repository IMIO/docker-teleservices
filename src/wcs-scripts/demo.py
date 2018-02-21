# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/var/lib/wcs/scripts')
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')
import re

from datetime import datetime
from time import mktime
from wcs.formdef import FormDef

if 'town' in sys.modules:
    del sys.modules['town']

import town


class Demo(town.Town):

    def __init__(self):
        super(Demo, self).__init__(variables=globals())

    # form_slug = le slug du formulaire
    # user_name_identifier_0, = identifiant unique de l'utilisateur
    # dic_params = un dictionnaire de parametres
    #    parametres accepte :
    #        - year:int, month:int
    #    sample : dic_params = {'year':2018, 'month':3}
    # dic_extra_fields = un dictionnaire de varname du formulaire et la valeur attendue
    #    sample : dic_extra_fields = {'rue':'du calvaire', 'cp':'4000'}
    #    retournera les formulaires qui ont une variable rue et une variable cp dont les valeurs sont specifies.
    def get_user_forms_with_params(self, form_slug, user_name_identifier_0, dic_params, dic_extra_fields=None):
    cpt = 0
    s = "lambda field: field.get_user().name_identifiers[0] == '{0}'".format(user_name_identifier_0)
    if 'year' in dic_params:
        s += " and field.receipt_time.tm_year == {0}".format(dic_params['year'])
    if 'month' in dic_params:
        s += " and field.receipt_time.tm_mon == {0}".format(dic_params['month'])
    f = eval(s)
    for formdef in FormDef.select(lambda form: form.internal_identifier== form_slug):
        for formdata in formdef.data_class().select(f):
                # (field for field in formdef.get_all_fields() if field.varname is not None and field.varname in lst_extra_fields)
                if dic_extra_fields is not None:
                    for field in formdef.get_all_fields():
                        if field.varname is not None and field.varname in dic_extra_fields and formdata.get_field_view_value(field) == dic_extra_fields[field.varname]:
                        cpt = cpt + 1
                else:
                    cpt = cpt + 1
        return str(cpt)

current_commune = Demo()
function = args[0]

functionList = {function: getattr(current_commune,function)}
if args[1] is not None:
    parameters = args[1]
    if isinstance(parameters, dict):
        result = functionList[function](**parameters)
    else:
        params = args[1:]
        result = functionList[function](*params)
else:
    result = functionList[function]()
