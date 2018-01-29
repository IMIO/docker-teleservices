# Test script WCS to export 1 specific form to "csv"
# sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2
# sudo -u wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=lalouviere-formulaires.guichet-citoyen.be extra_scolair_csv.py
# arg : commande_tickets_repas or commande_cartes_garderie

import csv
import sys
from time import mktime
from datetime import datetime
from wcs import sql
from wcs.formdef import FormDef

dicforms = {
    'commande_tickets_repas':'Commande de tickets repas',
    'commande_cartes_garderie':'Commande de cartes de garderie'
}

for formdef in FormDef.select(lambda x: x.name== dicforms[sys.argv[1]]):
    for formdata in formdef.data_class().select():
        columns = []
        columns.append(formdata.get_display_id()) # identifiant du formulaire
        creation_date = datetime.fromtimestamp(mktime(formdata.receipt_time))
        columns.append(creation_date.strftime('%d/%m/%Y %H:%M:%S'))
        last_update_date = datetime.fromtimestamp(mktime(formdata.last_update_time))
        columns.append(last_update_date.strftime('%d/%m/%Y %H:%M:%S'))
        columns.append(formdata.user.get_display_name() if formdata.user else '-')
        for field in formdef.get_all_fields(): # les autres champs
            if not hasattr(field, 'get_view_value'): # sauf les titres, etc.
                continue
            if field.in_listing or field.varname == 'nom_eleve' or field.varname == 'prenom_eleve':
                field_value = formdata.get_field_view_value(field) or ''
                if hasattr(field,'get_display_value') and field.get_display_value(formdata.get_field_view_value(field)) is not None:
                    field_value = field.get_display_value(formdata.get_field_view_value(field))
                columns.append(field_value)

        with open('/var/tmp/{}.csv'.format(sys.argv[1]), 'a') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter='|',
                            quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            csvwriter.writerow(columns)

