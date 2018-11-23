# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
import sys
sys.path.insert(0, '/var/lib/wcs/scripts')
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')
import re

if 'town' in sys.modules:
    del sys.modules['town']

import town


class Tintigny(town.Town):

    def __init__(self):
        super(Tintigny, self).__init__(variables=globals())


def next_weekday(self, d, weekday, periode):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += periode * 7
    return {'from':d + timedelta(days_ahead),'to':d + timedelta(days_ahead + 6)}

# if current_date is > Thirday 9:00 so can not command meal for next week.
def repas_valid_date(self, jour_de_reference, heure_de_reference, nb_sem_to_skip_dans_les_delais, nb_sem_to_skip_hors_delais):
    now = datetime.today()
    current_day = datetime.today().weekday()
    week = {0:'monday', 1:'tuesday', 2:'wednesday', 3:'thirday', 4:'friday', 5:'saturday', 6:'sunday'}
    if week.get(current_day) < jour_de_reference or (week.get(current_day) == jour_de_reference and now.hour <= int(heure_de_reference)):
        # print 'On est dans les temps pour la periode + {}'.format(nb_sem_to_skip_dans_les_delais,)
        periode = next_weekday(now, 0, nb_sem_to_skip_dans_les_delais,)
        # print str(periode)        
        return periode
    else:
        # print 'Trop tard, ce sera pour la periode + {}'.format(nb_sem_to_skip_hors_delais)
        periode = next_weekday(now, 0, nb_sem_to_skip_hors_delais)
        # print str(periode)
        return periode

if globals().get('args') is None:
    # repas_valid_date('thirday','9',1,2)
    print '.'
else:
    current_commune = Tintigny()
    function = args[0]
    parameters = args[1]
    functionList = {function: getattr(current_commune,function)}
    if len(args) > 1:
        if isinstance(parameters, dict):
            result = functionList[function](**parameters)
        else:
            params = args[1:]
            result = functionList[function](*params)
    else:
        result = functionList[function]()

