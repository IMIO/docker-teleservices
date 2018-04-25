# -*- coding: utf-8 -*-
from decimal import Decimal
import sys
sys.path.insert(0, '/var/lib/wcs/scripts')
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')
import re

if 'town' in sys.modules:
    del sys.modules['town']

import town


class Waterloo(town.Town):

    def __init__(self):
        super(Waterloo, self).__init__(variables=globals())

    def centre_recreatif_compute(self, nb_enfants, lst_week_choices):
        total = Decimal('0')
        tarif_appliquer = None
        if int(nb_enfants) == 1:
            tarif_appliquer = 'prix1'
        if int(nb_enfants) == 2:
            tarif_appliquer = 'prix2'
        if int(nb_enfants) >= 3:
            tarif_appliquer = 'prix3'
        # format du prix d'un centre recreatif pour un enfant
        # form_var_semaineE1_0_prix1
        for enfant in range(1,int(nb_enfants) + 1):
            if lst_week_choices[enfant - 1] is not None:
                nb_stages = len(lst_week_choices[enfant - 1])
                for stage in range(0, nb_stages):
                    varname = 'form_var_semaineE{0}_{1}_{2}'.format(enfant, stage, tarif_appliquer)
                    price_for_current_stage_and_child = globals().get(varname)
                    if price_for_current_stage_and_child is not None:
                        total = total + Decimal(price_for_current_stage_and_child)
                    else:
                        total = 'error : child {0}, var {1}, value = {2}'.format(enfant, varname, price_for_current_stage_and_child)
                        break
            else:
                total = 'error : child {0}'.format(enfant)
                break
        return str(total)

current_commune = Waterloo()
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
