# -*- coding: utf-8 -*-
from decimal import Decimal
import sys
sys.path.insert(0, '/var/lib/wcs/scripts')
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')
import re

if 'town' in sys.modules:
    del sys.modules['town']

import town

class children(object):
    def __init__(self, num_child, num_week, price, lst_activites):
        self.num_child = naum_child
        self.num_week = num_week
        self.price = price
        self.lst_activites = lst_activites

class Waterloo(town.Town):
    description = ''

    def __init__(self):
        super(Waterloo, self).__init__(variables=globals())

    @classmethod
    def centre_recreatif_compute(cls, nb_enfants, lst_week_choices, promotion='Non'):
        total = Decimal('0')
        tarif_appliquer = None
        details = ''
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
                details += 'Enfant {0}<ul>'.format(enfant)
                for stage in range(0, nb_stages):
                    semaine = globals().get('form_var_semaineE{0}'.format(enfant)).split(',')[stage]
                    price_varname = 'form_var_semaineE{0}_{1}_{2}'.format(enfant, stage, tarif_appliquer)
                    price_for_current_stage_and_child = globals().get(price_varname)
                    if price_for_current_stage_and_child is not None:
                        details += '<li>{0} - {1} Eur</li>'.format(semaine, price_for_current_stage_and_child)
                        total = total + Decimal(price_for_current_stage_and_child)
                    else:
                        total = 'error : Stage : child {0}, var {1}, value = {2}'.format(enfant, price_varname, price_for_current_stage_and_child)
                        break
                details += '</ul>'
            else:
                total = 'error : Stage : child {0}'.format(enfant)
                break
        cls.description += '<p>-------------</p><p><b>Semaines de plaine :</b></p>{0}'.format(details)
        return str(total) if promotion == 'Non' else '0.00' if globals().get('form_var_lst_promo_raw') == '1' else str(total / 2)

    @classmethod
    def centre_recreatif_activites_compute(cls, nb_enfants, lst_activites_choices):
        total = Decimal('0')
        # format du prix d'une activite par enfant
        # form_var_activite_comp_E1_0_prix
        details = ''
        has_activite = False
        for enfant in range(1,int(nb_enfants) + 1):
            if lst_activites_choices[enfant - 1]:
                details += 'Enfant {0}<ul>'.format(enfant)
                nb_activites = len(lst_activites_choices[enfant - 1])
                for activite in range(0, nb_activites):
                    activite_text = globals().get('form_var_activite_comp_E{0}'.format(enfant)).split(',')[activite]
                    price_varname = 'form_var_activite_comp_E{0}_{1}_prix'.format(enfant, activite)
                    price_for_current_activite_and_child = globals().get(price_varname)
                    if price_for_current_activite_and_child is not None:
                        has_activite = True
                        details += '<li>{0} - {1} Eur</li>'.format(activite_text, price_for_current_activite_and_child)
                        total = total + Decimal(price_for_current_activite_and_child)
                    else:
                        total = 'error1 : Activite : child {0}, var {1}, value = {2}'.format(enfant, price_varname, price_for_current_activite_and_child)
                        break
                details = '{0}{1}'.format(details,'</ul>')
        if has_activite is True:
            cls.description += '<p>-------------</p><p><b>Activites complementaires :</b></p>{0}'.format(details)

        return str(total)

    @classmethod
    def centre_recreatif_supp_piscine_13_ans(cls, lst_birthday_children, supplement=2):
        supp_piscine = 0
        from datetime import datetime
        from dateutil import relativedelta
        num_enfant = 1
        has_swimming_pool = False
        details = ''
        for birthday in lst_birthday_children:
            if birthday is not None and len(birthday) > 0:
                dt_birthday = datetime.strptime(birthday, '%d/%m/%Y')
                today = datetime.today()
                difference = relativedelta.relativedelta(today, dt_birthday) + 1
                if difference.years >= 13:
                    has_swimming_pool = True
                    details += '<ul><li>Enfant {0}  : {1} Eur</li></ul>'.format(num_enfant, supplement)
                    supp_piscine = supp_piscine + supplement
            num_enfant = num_enfant + 1
        if has_swimming_pool is True:
            cls.description += '<p>-------------</p><p><b>Frais de piscine :</b></p>{0}'.format(details)
        return supp_piscine

    def get_centre_recreatif_activites(self, lst_week_choices, datasource):
        new_datasource = []
        for item in datasource:
            for semaine in lst_week_choices:
                if semaine in item.get('id'):
                    new_datasource.append(item)
        return new_datasource

    def generate_structured_communication(self, transaction_id):
        split = transaction_id.split('-')
        transaction_id = split[0] + split[1] + str(sum([ int(c) for c in split[0] ]))
        count = 10 - len(str(transaction_id))
        for i in range(0,count):
            transaction_id = "{}{}".format('0',transaction_id)
        control = int(transaction_id) % 97
        str_control = str(control)
        if control < 10:
            str_control = "{}{}".format("0",str_control)
        com = "{}{}".format(transaction_id, str_control)
        # if int(com[:9]) % 97 == int(com[-2:]:
        # test if valid structured comm.
        return "{}/{}/{}".format(com[0:3], com[3:7], com[7:12])


if globals().get('args') is None:
    w = Waterloo()
    print str(w.centre_recreatif_supp_piscine_13_ans(['01/01/2005','','10/10/2016','02/02/2004']))
    print str(w.generate_structured_communication('34-45'))
else:
    if args[0] == 'get_payement_details':
        nb_children = globals().get('form_var_NB_Enfants') or 0
        lst_week_choices = [globals().get('form_var_semaineE1_raw'), globals().get('form_var_semaineE2_raw'), globals().get('form_var_semaineE3_raw'), globals().get('form_var_semaineE4_raw'), globals().get('form_var_semaineE5_raw'), globals().get('form_var_semaineE6_raw')] or []
        lst_activites_choices = [globals().get('form_var_activite_comp_E1_raw'), globals().get('form_var_activite_comp_E2_raw'), globals().get('form_var_activite_comp_E3_raw'), globals().get('form_var_activite_comp_E4_raw'), globals().get('form_var_activite_comp_E5_raw'), globals().get('form_var_activite_comp_E6_raw')] or []
        lst_birthday_children = [globals().get('form_var_birthdayE1'),  globals().get('form_var_birthdayE2'), globals().get('form_var_birthdayE3'), globals().get('form_var_birthdayE4'), globals().get('form_var_birthdayE5'), globals().get('form_var_birthdayE6')] or []
        w = Waterloo()
        w.centre_recreatif_compute(nb_children, lst_week_choices)
        w.centre_recreatif_activites_compute(nb_children, lst_activites_choices)
        w.centre_recreatif_supp_piscine_13_ans([globals().get('form_var_birthdayE1'),globals().get('form_var_birthdayE2'),globals().get('form_var_birthdayE3'),globals().get('form_var_birthdayE4'),globals().get('form_var_birthdayE5'),globals().get('form_var_birthdayE6')])
        result = '<p>{0}</p>'.format(Waterloo.description)
    else:
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

