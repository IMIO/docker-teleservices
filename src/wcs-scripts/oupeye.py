# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/var/lib/wcs/scripts')
import re

if 'town' in sys.modules:
    del sys.modules['town']

import town


class Oupeye(town.Town):

    def __init__(self):
        super(Oupeye, self).__init__(variables=globals())
        self.lst_motifs_dispo = globals().get('form_option_motifs_disponibles_structured')

    def autorisation_voyage_enfants_concernes(self):
        # enfants_concernes = variables.get('form_var_tab_enfants_concernes')
        return "aaa" # enfants_concernes

    def motif_compute(self, selected_motifs_var):
        lst_prices = [float(motif['price']) for motif in self.lst_motifs_dispo if motif['id'] in form_var_motif_raw]
        return sum(lst_prices)

current_commune = Oupeye()
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

