# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')
import re
import pdb

if 'town' in sys.modules:
    del sys.modules['town']

import town


class Mouscron(town.Town):

    def __init__(self):
        super(Oupeye, self).__init__(variables=globals())
        self.lst_motifs_dispo = globals().get('form_option_motifs_disponibles_structured')


current_commune = Mouscron()
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
