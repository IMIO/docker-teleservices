# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/var/lib/wcs/scripts')
import re

if 'town' in sys.modules:
    del sys.modules['town']

import town


class Commune(town.Town):

    def __init__(self):
        super(Namur, self).__init__(variables=globals())

current_commune = Commune()
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
