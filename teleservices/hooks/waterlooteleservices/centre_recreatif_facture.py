# -*- coding: utf-8 -*-
# sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2
# sudo -u wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=waterloo-formulaires.guichet-citoyen.be centre_recreatif_facture.py waterloo_facture

import csv
from decimal import Decimal
import re
import sys
from time import mktime
from datetime import datetime
from wcs.formdef import FormDef


lst_keeping_ids = ['1', '2', '17', '18', '19', '20', '21', '151', '152', '154', '179', '180', '182', '208', '208', '210', '292', '293', '295', '264', '265', '267', '236', '237', '239']

responsable = ['1', '2']
adresse_responsable = ['17', '18', '19'] #, '20', '21']
#rue = '17'
#numero = '18'
#boite = '19'

cp = '20'
localite = '21'

nb_enfants_by_resp = '90'
child1 = ['151', '152']
child2 = ['179', '180']
child3 = ['207', '208']
child4 = ['292', '293']
child5 = ['264', '265']
child6 = ['236', '237']

birth_child1 = '154'
birth_child2 = '182'
birth_child3 = '210'
birth_child4 = '295'
birth_child5 = '267'
birth_child6 = '239'

semainesE1 = '176'
semainesE2 = '204'
semainesE3 = '232'
semainesE4 = '317'
semainesE5 = '289'
semainesE6 = '261'

promotion = '54' # None, Oui, Non

has_promotion = False

str_semainesE1 = '' 
str_semainesE2 = ''
str_semainesE3 = ''
str_semainesE4 = ''
str_semainesE5 = ''
str_semainesE6 = ''

str_responsable = ''
str_child1 = ''
str_child2 = '' 
str_child3 = ''
str_child4 = ''
str_child5 = ''
str_child6 = ''

str_birth_child1 = ''
str_birth_child2 = ''
str_birth_child3 = ''
str_birth_child4 = ''
str_birth_child5 = ''
str_birth_child6 = ''
str_adresse_responsable = ''
str_cp = ''
str_localite = ''
get_nb_childs = 0


totalE1 = Decimal('0')
totalE2 = Decimal('0')
totalE3 = Decimal('0')
totalE4 = Decimal('0')
totalE5 = Decimal('0')
totalE6 = Decimal('0')

intitules = []
cpt = 0

total = [0,0,0,0,0,0]

LISTING = []
user_id = -1

def new_csv_line(columns):
    with open('/var/tmp/{}.csv'.format(sys.argv[1]), 'a') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='|',
                            quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        csvwriter.writerow(columns)

# new_csv_line(["Nom et prénom du responsable", "Adresse du reponsable", "Prénom et nom de l\'enfant", "Date de naissance", "Semaine(s) de plaine", "Total inscriptions"])
new_csv_line(["Nom et prénom du responsable", "Adresse", "Code postal", "Ville", "Prénom et nom de l\'enfant", "Date de naissance", "Semaine(s) de plaine", "Total inscriptions"])

# selection du form
for formdef in FormDef.select(lambda x: x.id=='34', order_by='-receipt_time'):
    # import ipdb;ipdb.set_trace()
    # balayage des demandes
    for formdata in formdef.data_class().select(lambda d: d.status!='draft', order_by='f1, f2, f151, f152, f179, f180, f207, f208, f292, f293, f264, f265, f236, f237'):
        user_id = formdata.user_id
        # balayage des field
        for field in formdef.get_all_fields(): # les autres champs
            if field.id in responsable:
                if hasattr(field, 'get_display_value'):
                    str_responsable = '{} {}'.format(str_responsable, field.get_display_value(formdata.get_field_view_value(field)))
                else:
                    str_responsable = '{} {}'.format(str_responsable, field.get_view_value(formdata.get_field_view_value(field)))

            if field.id in adresse_responsable:
                if field.id == '19':
                    str_adresse_responsable = '{} (b{})'.format(str_adresse_responsable, field.get_view_value(formdata.get_field_view_value(field)))
                else:
                    str_adresse_responsable = '{} {}'.format(str_adresse_responsable, field.get_view_value(formdata.get_field_view_value(field)))

            if field.id == cp:
                str_cp = field.get_view_value(formdata.get_field_view_value(field))

            if field.id == localite:
                str_localite = field.get_view_value(formdata.get_field_view_value(field))

            if field.id == promotion:
                # contient le nb d'enfants inscris a cette plaine.
                str_promo = field.get_view_value(formdata.get_field_view_value(field)).upper() 
                has_promotion = True if str_promo == "OUI" else False

            if field.id == nb_enfants_by_resp:
                # contient le nb d'enfants inscris a cette plaine.
                get_nb_childs = int(field.get_view_value(formdata.get_field_view_value(field)) or '1')
###################################################
            if field.id  in child1 and field.get_view_value(formdata.get_field_view_value(field)) != '': 
                str_child1 = '{} {}'.format(str_child1, field.get_view_value(formdata.get_field_view_value(field)))

            if field.id  in child2 and field.get_view_value(formdata.get_field_view_value(field)) != '': 
                str_child2 = '{} {}'.format(str_child2, field.get_view_value(formdata.get_field_view_value(field)))

            if field.id  in child3 and field.get_view_value(formdata.get_field_view_value(field)) != '': 
                str_child3 = '{} {}'.format(str_child3, field.get_view_value(formdata.get_field_view_value(field)))

            if field.id  in child4 and field.get_view_value(formdata.get_field_view_value(field)) != '': 
                str_child4 = '{} {}'.format(str_child4, field.get_view_value(formdata.get_field_view_value(field)))

            if field.id  in child5 and field.get_view_value(formdata.get_field_view_value(field)) != '': 
                str_child5 = '{} {}'.format(str_child5, field.get_view_value(formdata.get_field_view_value(field)))

            if field.id  in child6 and field.get_view_value(formdata.get_field_view_value(field)) != '': 
                str_child6 = '{} {}'.format(str_child6, field.get_view_value(formdata.get_field_view_value(field)))
####################################################
            if field.id == birth_child1 and field.get_view_value(formdata.get_field_view_value(field)) != '': 
                str_birth_child1 = field.get_view_value(formdata.get_field_view_value(field))

            if field.id == birth_child2 and field.get_view_value(formdata.get_field_view_value(field)) != '': 
                str_birth_child2 = field.get_view_value(formdata.get_field_view_value(field))

            if field.id == birth_child3 and field.get_view_value(formdata.get_field_view_value(field)) != '': 
                str_birth_child3 = field.get_view_value(formdata.get_field_view_value(field))

            if field.id == birth_child4 and field.get_view_value(formdata.get_field_view_value(field)) != '': 
                str_birth_child4 = field.get_view_value(formdata.get_field_view_value(field))

            if field.id == birth_child5 and field.get_view_value(formdata.get_field_view_value(field)) != '': 
                str_birth_child5 = field.get_view_value(formdata.get_field_view_value(field))

            if field.id == birth_child6 and field.get_view_value(formdata.get_field_view_value(field)) != '': 
                str_birth_child6 = field.get_view_value(formdata.get_field_view_value(field))
####################################################
            price_key = 'prix'
            if get_nb_childs == 1: 
                price_key = 'prix1'
            if get_nb_childs == 2:
                price_key = 'prix2'
            if get_nb_childs >= 3:
                price_key = 'prix3'
            if field.id  == semainesE1 and field.get_view_value(formdata.get_field_view_value(field)) != '':
                str_semainesE1 = field.get_view_value(formdata.get_field_view_value(field))
                for stage in formdata.data.get('176_structured'):
                    totalE1 = totalE1 + Decimal(stage.get(price_key) or '0')
                totalE1 = totalE1 / 2 if has_promotion == True else totalE1

            if field.id  == semainesE2 and field.get_view_value(formdata.get_field_view_value(field)) != '': 
                str_semainesE2 = field.get_view_value(formdata.get_field_view_value(field))
                for stage in formdata.data.get('204_structured'):
                    totalE2 = totalE2 + Decimal(stage.get(price_key) or '0')
                totalE2 = totalE2 / 2 if has_promotion == True else totalE2

            if field.id  == semainesE3 and field.get_view_value(formdata.get_field_view_value(field)) != '': 
                str_semainesE3 = field.get_view_value(formdata.get_field_view_value(field))
                for stage in formdata.data.get('232_structured'):
                    totalE3 = totalE3 + Decimal(stage.get(price_key) or '0')
                totalE3 = totalE3 / 2 if has_promotion == True else totalE3

            if field.id  == semainesE4 and field.get_view_value(formdata.get_field_view_value(field)) != '': 
                str_semainesE4 = field.get_view_value(formdata.get_field_view_value(field))
                for stage in formdata.data.get('317_structured'):
                    totalE4 = totalE4 + Decimal(stage.get(price_key) or '0')
                totalE4 = totalE4 / 2 if has_promotion == True else totalE4

            if field.id  == semainesE5 and field.get_view_value(formdata.get_field_view_value(field)) != '': 
                str_semainesE5 = field.get_view_value(formdata.get_field_view_value(field))
                for stage in formdata.data.get('289_structured'):
                    totalE5 = totalE5 + Decimal(stage.get(price_key) or '0')
                totalE5 = totalE5 / 2 if has_promotion == True else totalE5

            if field.id  == semainesE6 and field.get_view_value(formdata.get_field_view_value(field)) != '': 
                str_semainesE6 = field.get_view_value(formdata.get_field_view_value(field))
                for stage in formdata.data.get('261_structured'):
                    totalE6 = totalE6 + Decimal(stage.get(price_key) or '0')
                totalE6 = totalE6 / 2 if has_promotion == True else totalE6
        
        columns = []
        columns.append(str_responsable)
        columns.append(str_adresse_responsable)
        columns.append(str_cp)
        columns.append(str_localite)
        columns.append(str_child1)
        columns.append(str_birth_child1)
        columns.append(str_semainesE1.replace('_2018',''))
        columns.append(str(totalE1))
        columns.append(str(user_id))
        #new_csv_line(columns)
        LISTING.append(columns) 
        columns = []
        if get_nb_childs == '':
            get_nb_childs = 1
        if int(get_nb_childs) > 1:
            columns.append(str_responsable)
            columns.append(str_adresse_responsable)
            columns.append(str_cp)
            columns.append(str_localite)
            columns.append(str_child2)
            columns.append(str_birth_child2)
            columns.append(str_semainesE2.replace('_2018',''))
            columns.append(str(totalE2))
            columns.append(str(user_id))
            #new_csv_line(columns)
            LISTING.append(columns) 
            columns = []

        if int(get_nb_childs) > 2:
            columns.append(str_responsable)
            columns.append(str_adresse_responsable)
            columns.append(str_cp)
            columns.append(str_localite)
            columns.append(str_child3)
            columns.append(str_birth_child3)
            columns.append(str_semainesE3.replace('_2018',''))
            columns.append(str(totalE3))
            columns.append(str(user_id))
            #new_csv_line(columns)
            LISTING.append(columns) 
            columns = []

        if int(get_nb_childs) > 3:
            columns.append(str_responsable)
            columns.append(str_adresse_responsable)
            columns.append(str_cp)
            columns.append(str_localite)
            columns.append(str_child4)
            columns.append(str_birth_child4)
            columns.append(str_semainesE4.replace('_2018',''))
            columns.append(str(totalE4))
            #new_csv_line(columns)
            columns.append(str(user_id))
            LISTING.append(columns) 
            columns = []

        if int(get_nb_childs) > 4:
            columns.append(str_responsable)
            columns.append(str_adresse_responsable)
            columns.append(str_cp)
            columns.append(str_localite)
            columns.append(str_child5)
            columns.append(str_birth_child5)
            columns.append(str_semainesE5.replace('_2018',''))
            columns.append(str(totalE5))
            columns.append(str(user_id))
            #new_csv_line(columns)
            LISTING.append(columns) 
            columns = []

        if int(get_nb_childs) > 5:
            columns.append(str_responsable)
            columns.append(str_adresse_responsable)
            columns.append(str_cp)
            columns.append(str_localite)
            columns.append(str_child6)
            columns.append(str_birth_child6)
            columns.append(str_semainesE6.replace('_2018',''))
            columns.append(str(totalE6))
            columns.append(str(user_id))
            #new_csv_line(columns)
            LISTING.append(columns) 
            columns = []

        has_promotion = False

        str_responsable = ''
        str_adresse_responsable = ''
        str_cp = ''
        str_localite = ''
        str_child1 = ''
        str_child2 = '' 
        str_child3 = ''
        str_child4 = ''
        str_child5 = ''
        str_child6 = ''

        str_birth_child1 = ''
        str_birth_child2 = ''
        str_birth_child3 = ''
        str_birth_child4 = ''
        str_birth_child5 = ''
        str_birth_child6 = ''

        str_semainesE1 = ''
        str_semainesE2 = ''
        str_semainesE3 = ''
        str_semainesE4 = ''
        str_semainesE5 = ''
        str_semainesE6 = ''

        totalE1 = Decimal('0')
        totalE2 = Decimal('0')
        totalE3 = Decimal('0')
        totalE4 = Decimal('0')
        totalE5 = Decimal('0')
        totalE6 = Decimal('0')

import operator
# print sorted(LISTING, key=operator.itemgetter(1,4))

LISTING_COPY = sorted(LISTING, key=operator.itemgetter(0,4))
NEW_LISTING = []
id_responsable = ''
nom_responsable = ''
enfant = ''
cpt = 0
for ligne in LISTING_COPY:
    # on est sur une ligne avec m enfant. donc on supprime la ligne et on update la ligne precedente pour append semaine et somme total.
    if id_responsable == ligne[8] and nom_responsable == ligne[0] and enfant.upper() == ligne[4].upper():
        NEW_LISTING[-1][6] = '{},{}'.format(LISTING_COPY[cpt -1][6],ligne[6])
        NEW_LISTING[-1][7] = Decimal(LISTING_COPY[cpt -1][7]) + Decimal(ligne[7])
        #LISTING_COPY[cpt -1][6] = '{},{}'.format(LISTING_COPY[cpt -1][6],ligne[6])
        #LISTING_COPY[cpt -1][7] = Decimal(LISTING_COPY[cpt -1][7]) + Decimal(ligne[7])
        #del LISTING_COPY[cpt]
        #cpt = cpt - 1
    else:
        NEW_LISTING.append(ligne)
    id_responsable =  ligne[8]
    nom_responsable = ligne[0]
    enfant = ligne[4]
    cpt = cpt + 1


for ligne in sorted(NEW_LISTING, key=operator.itemgetter(0,4)):
    new_csv_line(ligne)
