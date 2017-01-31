# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')
import re
import pdb

if 'town' in sys.modules:
    del sys.modules['town']

import town


class Namur(town.Town):

    def __init__(self):
        super(Namur, self).__init__(variables=globals())

    # Get a readable list formated like : [('id1','libelle1','price1'),('id2','libelle2','price2')]
    # return a less readable but more functionnal list like :  [('id1_price1','libelle1'),('id2_price2','libelle2')] to populate multiselectlist or multicheckboxlist.
    def get_list_with_formated_id_price(self, choices):
        try:
            new_list = [(elem[0] + "_" + elem[2], elem[1]) for elem in choices]
            return new_list
        except:
            return 'Invalid parameters. Please, verify your list of choices {\'choices\':[(\'ID1\',\'TITLE1\',\'PRICE1\'), (\'ID2\',\'TITLE2\',\'PRICE2\'),...]}'

    # Compute price tanks to id_price
    # select must be the less readable list : (id1_price1, id2_price2, id3_price3)
    def compute_prices_list(self,select):
        try:
            return sum([int((elem.split('_'))[1]) for elem in select])
        except:
            return 'Invalid result'

    # Permet de transformer une datasrc imagin�e comme ceci : [[id1,title1,prix1], [id2,title2, prix2]]
    # vers une liste comme celle-ci : [[id1_prix1, title1], [id2_prix2, title2]]
    def datasource_with_price_and_id(self, datasrc):
        nouvelle_liste = []
        for item in datasrc:
            new_item = [item[0] + "_" + str(item[2]), item[1]]
            nouvelle_liste.append(new_item)
        return nouvelle_liste

    # Permet, à partir d'une liste alimentée par un dictionnaire avec, par exemple, un id, un text et un prix
    # et à partir d'un tableau qui reprend certains intitulés de la liste et qui demande, par exemple un nombre d'exemplaire pour les items de la liste
    # de renvoyer le total
    # table_var : La variable du tableau qui contient le nb d'exemplaires pour les articles de la liste à choix multiple préalablement sélectionnés.
    # list_var_raw : La variable "raw" de la liste d'item
    # list_name : str qui contient le nom de la variable de la liste d'item
    # rich_list_properties_name : Notre liste, alimentée par un dictionnaire est enrichie par une propriétés "price" ==> rich_liste_properties_name = "price" 
    # table_col : Spécifie la colonne du tableau qui sera utilisée dans le calcul avec la propriété enrichie de la liste.
    def compute_price(self, table_var, list_var_raw, list_name, rich_list_properties_name, table_col=0):
        filtered_table = []
        for elem in table_var:
            try:
                filtered_table.append(int(elem[table_col]))
            except:
                pass
        list_motifs = []
        i = 0
        while i<len(list_var_raw):
            list_motifs.append(int(globals().get(list_name + "_" + str(i) + "_" + rich_list_properties_name)))
            i = i+1
        return str(sum(map(operator.mul, list_motifs, filtered_table)))

current_commune = Namur()
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
