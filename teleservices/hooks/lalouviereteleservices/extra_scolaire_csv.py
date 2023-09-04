# Test script WCS to export 1 specific form to "csv"
# sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2
# sudo -u wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=lalouviere-formulaires.guichet-citoyen.be extra_scolaire_csv.py
# arg : tickets_repas or cartes_garderies

import csv
import os
import re
import sys
from datetime import datetime
from os import path
from time import mktime

from wcs.formdef import FormDef

FORMS_DICT = {
    "tickets_repas": "Commande de tickets repas",
    "cartes_garderies": "Commande de cartes de garderie",
}
FILENAME = sys.argv[1]
FORM_FULLNAME = FORMS_DICT[FILENAME]
FILE_OPEN_METHOD = "w+"
SAVE_FILE_PATH = f"/var/tmp/{FILENAME}.csv"

# Verify if there is an argument or provide help
if len(sys.argv) < 2:
    print("Please provide an argument")
    print("arg : 'tickets_repas' or 'cartes_garderies'")
    sys.exit()

if path.exists(SAVE_FILE_PATH):
    os.remove(SAVE_FILE_PATH)


for form_def in FormDef.select(lambda x: x.name == FORM_FULLNAME):
    forms_data_full_list = form_def.data_class().select()
    for form_data in forms_data_full_list:
        # Status to filter :
        r = re.compile("Paiement effectu.*")
        # Checks if the creation_date is after 2019 and at least one name in
        # form_data.evolution matches the regular expression r
        # Convert receipt_time to datetime object
        creation_date = datetime.fromtimestamp(mktime(form_data.receipt_time))

        # This is initial code written by cboulanger. It's currently not working
        # since evolution.get_status().name is None on some elements. It blocks
        # the script from running and accomplishing its task.
        # I let it here for reference.
        #
        # creation_date = datetime.fromtimestamp(mktime(form_data.receipt_time))
        # if (
        #     creation_date.year > 2019
        #     and sum(
        #         1
        #         for _ in filter(
        #             r.match,
        #             [evolution.get_status().name for evolution in form_data.evolution],
        #         )
        #     )
        #     > 0
        # ):

        # Unlock solution starts here
        # This is a attempt to unlock the script. It's not working either with the
        # previous commenter part (see explanations above).
        if creation_date.year > 2019:
            status_names = [
                status.name
                for evolution in form_data.evolution
                if (status := evolution.get_status()) is not None
                and status.name is not None
            ]

            matching_count = sum(1 for _ in filter(r.match, status_names))

            if matching_count > 0:
                columns = []
                columns.append(form_data.get_display_id())  # identifiant du formulaire
                columns.append(creation_date.strftime("%d/%m/%Y %H:%M:%S"))
                last_update_date = datetime.fromtimestamp(
                    mktime(form_data.last_update_time)
                )
                columns.append(last_update_date.strftime("%d/%m/%Y %H:%M:%S"))
                columns.append(
                    form_data.user.get_display_name() if form_data.user else "-"
                )
                for field in form_def.get_all_fields():  # les autres champs
                    if not hasattr(field, "get_view_value"):  # sauf les titres, etc.
                        continue
                    if hasattr(field, "in_listing") and field.in_listing:
                        field_value = form_data.get_field_view_value(field) or ""
                    if hasattr(field, "include_in_listing") and (
                        field.include_in_listing
                        or field.varname == "nom_eleve"
                        or field.varname == "prenom_eleve"
                    ):
                        field_value = form_data.get_field_view_value(field) or ""
                        if (
                            hasattr(field, "get_display_value")
                            and field.get_display_value(
                                form_data.get_field_view_value(field)
                            )
                            is not None
                        ):
                            field_value = field.get_display_value(
                                form_data.get_field_view_value(field)
                            )
                        columns.append(field_value)
                if path.exists(SAVE_FILE_PATH):
                    FILE_OPEN_METHOD = "a"
                with open(
                    SAVE_FILE_PATH, FILE_OPEN_METHOD, encoding="utf-8"
                ) as csvfile:
                    csvwriter = csv.writer(
                        csvfile,
                        delimiter="|",
                        quoting=csv.QUOTE_MINIMAL,
                        lineterminator="\n",
                    )
                    csvwriter.writerow(columns)
