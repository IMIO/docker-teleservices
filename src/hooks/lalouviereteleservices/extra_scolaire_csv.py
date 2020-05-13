# Test script WCS to export 1 specific form to "csv"
# sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2
# sudo -u wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=lalouviere-formulaires.guichet-citoyen.be extra_scolaire_csv.py
# arg : tickets_repas or cartes_garderies

import csv
import re
import sys
from datetime import datetime
from os import path
from time import mktime
from wcs.formdef import FormDef

dicforms = {
    "tickets_repas": "Commande de tickets repas",
    "cartes_garderies": "Commande de cartes de garderie",
}
file_open_method = "w+"
for formdef in FormDef.select(lambda x: x.name == dicforms[sys.argv[1]]):
    for formdata in formdef.data_class().select():
        r = re.compile("Paiement effectu.*")
        if (
            sum(
                1
                for _ in filter(
                    r.match,
                    [evolution.get_status().name for evolution in formdata.evolution],
                )
            )
            > 0
        ):
            columns = []
            columns.append(formdata.get_display_id())  # identifiant du formulaire
            creation_date = datetime.fromtimestamp(mktime(formdata.receipt_time))
            columns.append(creation_date.strftime("%d/%m/%Y %H:%M:%S"))
            last_update_date = datetime.fromtimestamp(mktime(formdata.last_update_time))
            columns.append(last_update_date.strftime("%d/%m/%Y %H:%M:%S"))
            columns.append(formdata.user.get_display_name() if formdata.user else "-")
            for field in formdef.get_all_fields():  # les autres champs
                if not hasattr(field, "get_view_value"):  # sauf les titres, etc.
                    continue
                if hasattr(field, "in_listing") and field.in_listing:
                    field_value = formdata.get_field_view_value(field) or ""
                if hasattr(field, "include_in_listing") and (
                    field.include_in_listing
                    or field.varname == "nom_eleve"
                    or field.varname == "prenom_eleve"
                ):
                    field_value = formdata.get_field_view_value(field) or ""
                    if (
                        hasattr(field, "get_display_value")
                        and field.get_display_value(
                            formdata.get_field_view_value(field)
                        )
                        is not None
                    ):
                        field_value = field.get_display_value(
                            formdata.get_field_view_value(field)
                        )
                    columns.append(field_value)
            if path.exists("/var/tmp/{}.csv".format(sys.argv[1])):
                file_open_method = "a"
            with open(
                "/var/tmp/{}.csv".format(sys.argv[1]), file_open_method
            ) as csvfile:
                csvwriter = csv.writer(
                    csvfile,
                    delimiter="|",
                    quoting=csv.QUOTE_MINIMAL,
                    lineterminator="\n",
                )
                csvwriter.writerow(columns)
