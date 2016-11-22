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


  def validate_dynamic_tab_cells(self, table_var, id_colonne, regex_pattern, id_row = "-1"):
    retour = True
    id_col = int(id_colonne)
    try:
      if id_row == "-1":
        for item in table_var:
          value = item[id_col]
          if value == '' or value is None:
            value = "0"
          if re.match(regex_pattern, value) is None:
            return False
      else:
        id_r = int(id_row)
        if re.match(regex_pattern,table_var[id_r][id_col]) is None:
          retour = False
      return retour
    except:
      return False

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
