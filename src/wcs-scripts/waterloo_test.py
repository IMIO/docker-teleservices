# -*- coding: utf-8 -*-
import waterloo 

form_var_NB_Enfants = '3'
form_var_promotion = 'Non'
form_var_semaineE1 = 'S3 du 16 Juillet au 20 juillet 2018, S3 du 16 Juillet au 20 juillet 2018, S3 du 16 Juillet au 20 juillet 2018'
form_var_semaineE2 = 'S3 du 16 Juillet au 20 juillet 2018, S7 bla bla bla'
form_var_semaineE3 = 'S1 du 10 Juin au 20 juin 2018'
form_var_semaineE1_raw = ['S1_2018', 'S2_2018', 'S3_2018']
form_var_semaineE2_raw = ['S3_2018','S7_2018']
form_var_semaineE3_raw = ['S3_2018']
form_var_semaineE4_raw = None
form_var_semaineE5_raw = None
form_var_semaineE6_raw = None
form_var_activite_comp_E1 = 'walibi1,walibi2,walibi3'
form_var_activite_comp_E2 = 'walibi3,walibi7'
form_var_activite_comp_E3 = 'walibi1,walibi2'
form_var_activite_comp_E4 = None
form_var_activite_comp_E5 = None
form_var_activite_comp_E6 = None
form_var_activite_comp_E1_raw = ['S1_2018_1','S2_2018_2','S3_2018_1']
form_var_activite_comp_E2_raw = ['S3_2018_1', 'S7_2018_1']
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
datasource_activites_affichees = {"data": [{"text": "", "id": "S3_2018_1", "prix": "0"}, {"text": "Jeudi 19/07 : Walibi (pour les 8 \u00e012 ans) ou Mont Mosan (pour les 2,5 \u00e0 7 ans) \n(25 Eur )", "id": "S3_2018_2", "prix": "25"}, {"text": "Jeudi 19/07 : Walibi : \nj'ai d\u00e9j\u00e0 un abonnement \n(transport \u00e0 payer : 10 Eur). Veuillez envoyer une copie de l'abonnement par mail.", "id": "S3_2018_3", "prix": "10"}, {"text": "Jeudi 19/07 : Je ne participe pas \u00e0 la sortie et ne serais pas pr\u00e9sent au Centre R\u00e9cr\u00e9atif ce jour l\u00e0.", "id": "S3_2018_4", "prix": "0"}, {"text": "", "id": "S7_2018_1", "prix": "0"}, {"text": "Jeudi 16/08 : Visite de la ferme du Pr\u00e9vot pour les 2,5 \u00e0 5 ans \n(20 Eur)", "id": "S7_2018_2", "prix": "20"}, {"text": "Jeudi 16/08 : Koh Lanta fermier \u00e0 la ferme du Pr\u00e9vot pour les 6 \u00e0 12 ans (20 Eur)", "id": "S7_2018_3", "prix": "20"}, {"text": "Jeudi 16/08 : Je ne participe pas \u00e0 la sortie et ne serais pas pr\u00e9sent au Centre R\u00e9cr\u00e9atif ce jour l\u00e0. ", "id": "S7_2018_4", "prix": "0"}], "err": 0}

assert w.is_at_least_one_activity_by_week('E1', datasource_activites_affichees) == False
assert w.is_at_least_one_activity_by_week('E2', datasource_activites_affichees) == True

print w.description
# print "method total_desc = {0}".format(w.total_desc(0))
# print str(w.generate_structured_communication('34-45'))
