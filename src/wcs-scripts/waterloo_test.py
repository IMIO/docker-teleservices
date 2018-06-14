# -*- coding: utf-8 -*-
import waterloo 

form_var_NB_Enfants = '3'
form_var_promotion = 'Non'
form_var_semaineE1 = 'S3 du 16 Juillet au 20 juillet 2018, S3 du 16 Juillet au 20 juillet 2018, S3 du 16 Juillet au 20 juillet 2018'
form_var_semaineE2 = 'S3 du 16 Juillet au 20 juillet 2018, S2 du 25 Juin au 30 juin 2018'
form_var_semaineE3 = 'S1 du 10 Juin au 20 juin 2018'
form_var_semaineE1_raw = ['S1_2018', 'S2_2018', 'S3_2018']
form_var_semaineE2_raw = ['S3_2018','S2_2018']
form_var_semaineE3_raw = ['S3_2018']
form_var_semaineE4_raw = None
form_var_semaineE5_raw = None
form_var_semaineE6_raw = None
form_var_activite_comp_E1 = 'walibi,walibi2b,walibi2,walibi3'
form_var_activite_comp_E2 = 'walibi,walibi3'
form_var_activite_comp_E3 = 'walibi3,walibi4'
form_var_activite_comp_E4 = None
form_var_activite_comp_E5 = None
form_var_activite_comp_E6 = None
form_var_activite_comp_E1_raw = ['S1_2018_1','S2_2018_2','S2_2018_1','S3_2018_1']
form_var_activite_comp_E2_raw = ['S1_2018_1', 'S3_2018_1']
form_var_activite_comp_E3_raw = ['S3_2018_1','S3_2018_2']
form_var_activite_comp_E4_raw = None
form_var_activite_comp_E5_raw = None
form_var_activite_comp_E6_raw = None

lst_week_choices = [form_var_semaineE1_raw,
        form_var_semaineE2_raw,
        form_var_semaineE3_raw,
        form_var_semaineE4_raw,
        form_var_semaineE5_raw,
        form_var_semaineE6_raw]
lst_birthday_children = ['10/09/2007','01/01/2006','03/02/2011',None, None, None]
form_var_semaineE1_0_prix1 = 40
form_var_semaineE1_0_prix2 = 37.5
form_var_semaineE1_0_prix3 = 30
form_var_semaineE1_1_prix1 = 40
form_var_semaineE1_1_prix1 = 40
form_var_semaineE1_1_prix2 = 37.5
form_var_semaineE1_2_prix3 = 30
form_var_semaineE1_2_prix2 = 37.5
form_var_semaineE1_2_prix3 = 30
form_var_semaineE2_0_prix1 = 40
form_var_semaineE2_0_prix2 = 37.5
form_var_semaineE2_0_prix3 = 30
form_var_semaineE2_1_prix1 = 40
form_var_semaineE2_1_prix2 = 37.5
form_var_semaineE2_1_prix3 = 30
form_var_semaineE3_0_prix1 = 40
form_var_semaineE3_0_prix2 = 37.5
form_var_semaineE3_0_prix3 = 30
w = waterloo.Waterloo(globals())
w.cr_nb_enfants = form_var_NB_Enfants
w.cr_promotion = form_var_promotion
w.cr_lst_week_choices = lst_week_choices
w.cr_lst_birthday_children = lst_birthday_children

# Test promotion si n enfants participent à la meme semaine!
print str(w.centre_recreatif_compute(3 , lst_week_choices, 'Non'))
print str(w.centre_recreatif_compute(3 , lst_week_choices, 'Oui'))
print str(w.centre_recreatif_supp_piscine_5_ans(lst_birthday_children,
                                                lst_week_choices))
# assert exception de prix pour enfant de 6 ou 7 ans 
print str(w.centre_recreatif_piscine_exceptions(lst_birthday_children,
                                                lst_week_choices))

# une activité obligatoire par semaine pour 1 enfant
assert w.is_at_least_one_activity_by_week('E1') == True
assert w.is_at_least_one_activity_by_week('E2') == False


print w.description
# print "method total_desc = {0}".format(w.total_desc(0))
# print str(w.generate_structured_communication('34-45'))
