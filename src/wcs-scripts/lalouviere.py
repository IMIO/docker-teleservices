# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')

if 'town' in sys.modules:
    del sys.modules['town']

import town


class Lalouviere(town.Town):

    def __init__(self):
        super(Lalouviere, self).__init__(variables=globals())

    # Has been adapted from Liege.py. (La Louvière reused Pop/Etat Civil Liège's forms)
    def is_not_lalouviere_filtered_list(self, choices, is_not_lalouviere_filtered_list = [], forms_exceptions= []):
        if not self.user_zipcode:
            return choices
        if self.user_zipcode in ('7100',):
            return choices
        else:
            if self.form_slug in forms_exceptions:
                return choices
            else:
                return [x for i, x in enumerate(choices) if i in is_not_lalouviere_filtered_list

    def validate_dynamic_tab_cells(self, table_var, id_colonne, regex_pattern, id_row = "-1"):
        retour = True
        id_col = int(id_colonne)
        try:
            if id_row == "-1":
                for item in table_var:
                    value = item[id_col]
                    if value == '':
                        value = value.replace("","0")
                    if re.match(regex_pattern, value) is None:
                        retour = False
            else:
                id_r = int(id_row)
                if re.match(regex_pattern,table_var[id_r][id_col]) is None:
                    retour = False
            return retour
        except:
            return False

    # Permet de transformer une datasrc imagin�e comme ceci : [[id1,title1,prix1], [id2,title2, prix2]]
    # vers une liste comme celle-ci : [[id1_prix1, title1], [id2_prix2, title2]]
    def datasource_with_price_and_id(self, datasrc):
        nouvelle_liste = []
        for item in datasrc:
            new_item = [item[0] + "_" + str(item[2]), item[1]]
            nouvelle_liste.append(new_item)
        return nouvelle_liste


current_commune = Lalouviere()
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
