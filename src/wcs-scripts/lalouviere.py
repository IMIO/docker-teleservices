# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/var/lib/wcs/scripts')
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')

if 'town' in sys.modules:
    del sys.modules['town']

from datetime import date, datetime, timedelta
import town


class Lalouviere(town.Town):

    def __init__(self):
        super(Lalouviere, self).__init__(variables=globals())

    # Has been adapted from Liege.py (La Louvière reused Pop/Etat Civil Liège's forms)
    def is_not_lalouviere_filtered_list(self, choices, is_not_lalouviere_filtered_list = [], forms_exceptions= []):
        if not self.user_zipcode:
            return choices
        if self.user_zipcode in ('7100', '7110'):
            return choices
        else:
            if self.form_slug in forms_exceptions:
                return choices
            else:
                return [x for i, x in enumerate(choices) if i in is_not_lalouviere_filtered_list]

    # Has been adapted from Liege.py (La Louvière reused Pop/Etat Civil Liège's forms)
    def is_lalouviere_resident(self, choices, is_lalouviere_filtered_list = [], is_not_lalouviere_filtered_list = []):
        if not self.user_zipcode:
            return choices
        if self.user_zipcode in ('7100', '7110'):
            if len(is_lalouviere_filtered_list) > 0:
                return [x for i, x in enumerate(choices) if i in is_lalouviere_filtered_list]
            else:
                return choices
        else:
            if len(is_not_lalouviere_filtered_list) > 0:
                return [x for i, x in enumerate(choices) if i in is_not_lalouviere_filtered_list]
            else:
                return choices

    # Has been adapted from Liege.py (La Louvière reused Pop/Etat Civil Liège's forms)
    def test_lalouviere_and_return_text(self, is_lalouviere_text, is_not_lalouviere_text):
        if self.user_zipcode  in ('7100', '7110'):
            return is_lalouviere_text
        else:
            return is_not_lalouviere_text

    # Has been adapted from Liege.py (La Louvière reused Pop/Etat Civil Liège's forms)
    def verif_lalouviere_wedding(self, wedding_cities):
        if wedding_cities in lalouviere_cities or wedding_cities is None:
            return True
        else:
            return False
    # Has been adapted from Liege.py (La Louvière reused Pop/Etat Civil Liège's forms)
    def had_lalouviere_wedding(self, choices, is_not_lalouviere_filtered_list = []):
        if not self.user_wedding_cities:
            return choices
        if lalouviere_cities.intersection(self.user_wedding_cities.split('|')):
            return choices
        else:
            return [x for i, x in enumerate(choices) if i in is_not_lalouviere_filtered_list]


    # Has been adapted from Liege.py (La Louvière reused Pop/Etat Civil Liège's forms)
    def has_lalouviere_birthplace(self, choices, is_not_lalouviere_filtered_list = []):
        if not self.user_birthplace:
            return choices
        if self.user_birthplace in lalouviere_cities:
            return choices
        else:
            return [x for i, x in enumerate(choices) if i in is_not_lalouviere_filtered_list]

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

    # delta_option = 0 : timedelta between date1 and date2
    # delta_option = 1 : timedelta between date1 and date2 and sum w.e.
    # delta_option = 2 : timedelta between date1 and date2 and sum w.e. and sum legal holydays.
    def diff_dates_occupation_voie_publique(self, date1, date2, deadline=7, delta_option=2):
        try:
            legal_holidays = globals().get("form_option_legal_holidays")
            result = "False"
            today = datetime.today().strftime("%d/%m/%Y")
            total_duree_occupation = int(self.diff_dates(date1, date2))
            nb_extra_days = 0
            d1 = datetime.strptime(date1, '%d/%m/%Y')
            d2 = datetime.strptime(date2, '%d/%m/%Y')
            if delta_option in [1,2]:
                for single_date in (d1 + timedelta(n) for n in range(total_duree_occupation)):
                    if single_date.weekday() in [5,6]:
                        nb_extra_days = nb_extra_days + 1
            if delta_option == 2:
                for day in legal_holidays:
                    d = datetime.strptime(day[0], '%d/%m/%Y')
                    # 5 is saturday, 6 is sunday.
                    if d1 < d < d2 and d.weekday() not in [5,6]:
                        # calcul les jours non ouvrable dans la periode entre date1 et date2
                        nb_extra_days = nb_extra_days + 1
            if int(self.diff_dates(today, date1)) >= (deadline + nb_extra_days):
                    result = "True"
            return result
        except:
            return "diff_dates_occupation_error"

    # filtrage de mails pour une liste de dictionnaire telle que :
    #[{'id':'police','mail':'christophe.boulanger+1@imio.be','text':'la Police'},...]
    # varname = is a string like : 'formavis_var_liste_avis'
    # lst_ids = is a form var like : formavis_var_liste_avis_raw
    # "formavis_var_liste_avis_2_mail" will be the var that keep mail from index 2.
    def mail_filtering(self, varname, ignore_ids = [], auth_ids = []):
        is_there_ignore_ids = False if len(ignore_ids) == 0 else True
        is_there_auth_ids = False  if len(auth_ids) == 0 else True
        # Authorising list mails are stronger than ignoring list mails
        str_mails_to_send = ""
        lst_index_to_keep = []
        var_raw = globals().get('{}_{}'.format(varname,'raw'))
        if is_there_ignore_ids is True and is_there_auth_ids is True:
            is_there_ignore_ids = False
        if is_there_ignore_ids == True:
            lst_index_to_keep = [int(var_raw.index(elem)) for elem in var_raw if elem not in ignore_ids]
        else:
            lst_index_to_keep = [int(var_raw.index(elem)) for elem in var_raw if elem in auth_ids]
        for i in lst_index_to_keep:
            str_mails_to_send += "{};".format(globals().get("{}_{}_mail".format(varname, i)))
        return str_mails_to_send



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
