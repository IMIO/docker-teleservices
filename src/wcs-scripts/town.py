# -*- coding: utf-8 -*-
import datetime
import re
import pdb


class Town(object):

    def __init__(self, variables):
        self.class_name = 'Town'
        self.form_name = variables.get('form_name')
        self.user_zipcode = variables.get('session_user_var_zipcode')
        self.user_birthplace = variables.get('session_user_var_birthplace')
        self.user_wedding_cities = variables.get('session_user_var_wedding_cities') or ''
        self.user_title = variables.get('session_user_var_title')
        try:
            self.form_slug = variables.get('form_slug')
        except NameError:
            self.form_slug = None

    def get_form_slug(self):
        return self.form_slug

    def get_form_name(self):
        return self.form_name

    # Méthode qui ser à retourner un texte accompaggé d'un résultat.    
    # valeur : Un nombre
    # texte : un article (par exemple)
    # coeff : un coéfficient multiplicateur
    # unit : unité de mesure
    # return sample = "[2] [certficats de domicile] = [10 (valeur*coeff)] [€]"
    def txt_ifn_zero(self, valeur, texte, coeff = 1, unit = ""):
        if str(valeur) == "0":
            return ""
        else:
            return str(valeur) + " " + texte + " = " + str(int(valeur) * coeff)+ " " + unit

    def criteria_filtered_list(self, choices, value_to_test, criteria_to_test, choices_if_true, choices_if_false):
        if str(choices) not in choices_if_false:
            # patch for attestatin de milice Liege ... TODO 
            choices_if_false = [0]
        if value_to_test == criteria_to_test:
            return [x for i, x in enumerate(choices) if i in choices_if_true]
        else:
            return [x for i, x in enumerate(choices) if i in choices_if_false]

    # Return number of days between two date
    # date1 : oldest date '%d/%m/%Y' format
    # date2 : newest date '%d/%m/%Y' format
    # if date1 older than date2, you get a postivie number of days.
    # return = Number of day between date2 and date1 
    def diff_dates(self, date1, date2):
        try:
            d1 = datetime.datetime.strptime(date1, '%d/%m/%Y')
            d2 = datetime.datetime.strptime(date2, '%d/%m/%Y')
            diff = (d2 - d1).days
            return str(diff)
        except:
            return "diff_dates_error"

    # Try to sum each row from a given column in a table (each value from the given column must be integer)
    # table_var : this is the variable name of the table in forms.
    # id_colonne : the id of the column in the table!
    # price : default value = 1.
    # return =  [sum of all row in given column] * price.
    def compute_dynamic_tab(self, table_var, id_colonne, price = 1):
        result = 0
        if table_var is None:
            return str(result)
        else:
            try:
                id_col = int(id_colonne)
                for item in table_var:
                    value = item[id_col]
                    if value is None or value == "":
                        value = "0"
                    result = result + int(value)
                result = int(result) * int(price)
                return str(result)
            except:
                return "compute_dynamic_tab : error" + str(table_var)

    # Imaginons un tableau. Chaque ligne est un motif et, dans la cellule de chaque motif, on peut y mettre un nombre d'exemplaires. 
    # Il nous est impossible avec une telle représentation dans l'outil TS2 de faire un calcul directement sur le nombre d'exemplaire * 1 prix. (sauf si on affiche le prix en 2e colonne)
    # et de retourner un total complet.
    # Cette méthode apporte une solution à ce prolbème.
    # tab_var : Nom de la variable du tableau dans le formulaire
    # num_col : Numéro de colonne qui participe au calcul du résultat
    # memory_tab : Une liste avec la représentation en mémoire du tableau du formulaire [['id1','libelle1','price1'], ['id2','libelle2','price2'],..]
    def compute_tab_col(self, tab_var, num_col, memory_tab):
        error1 = "Erreur compute_tab_col : tableau en mem. different que tableau du formulaire."
        result = 0
        if len(tab_var) != len(memory_tab):
            result = error1
        else:
            cpt = 0
            for item in tab_var:
                try:
                    if item[int(num_col)] is None:
                        item = '0'
                    result = result + (int(item[int(num_col)]) * int(memory_tab[cpt][2]))
                    cpt = cpt + 1
                except:
                    result = "Erreur compute_tab_col"
        return str(result)

    # Use in Liege and Namur
    #
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

    def is_valid_belgian_nrn(self, nrn, can_be_none = 'False'):
        if can_be_none == 'True' and str(nrn) == "None":
            return True
        else:
            try:
                if nrn is None:
                    nrn = "0"
                return ((97 - int(nrn[:9]) % 97 == int(nrn[-2:])) or (97 - int("2" + nrn[:9]) % 97 == int(nrn[-2:])))
            except ValueError:
                return False

# à valider.
#  def is_valid_iban(self, iban):
#    ibanValidationModulo = 97
#    iban = iban.upper()
#    iban = iban.replace(" ","")
#    if len(iban) < 5:
#      return False
#    modifiedIban = iban[4:len(iban)] + iban[0:4]
#    numericIbanString = ""
#    for c in modifiedIban:
#      currentCharCode = ord(c)
#      # Integer
#      if (currentCharCode > 47) and (currentCharCode <  58):
#        numericIbanString = numericIbanString + c
#      # Char
#      elif (currentCharCode > 64) and (currentCharCode < 91):
#        value = currentCharCode - 65 + 10
#        numericIbanString = numericIbanString + str(value)
#      else:
#        return false;
#    previousModulo = 0;
#    for i in xrange(0,len(numericIbanString),5):
#      subpart = str(previousModulo) + "" + numericIbanString[i:i + 5]
#      previousModulo = int(subpart) % ibanValidationModulo
#    return previousModulo == 1
