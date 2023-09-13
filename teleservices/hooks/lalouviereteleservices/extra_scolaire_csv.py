"""
This will export some data from a specific form to a csv file.
Initially written by cboulanger, it was not working due to a bug in the
evolution.get_status().name part (see SUP-31982 and below for more details)

Args (wcsctl):
    $1: vhost
    $2: domain

Args (script):
    1: form name (tickets_repas or cartes_garderies)

Example:
sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript \
    --vhost=$1-formulaires.$2
sudo -u wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript \
    --vhost=lalouviere-formulaires.guichet-citoyen.be extra_scolaire_csv.py
"""
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

# Pylint points filename and file_open_method are constants and should be
# uppercase, but this is conventional and not strictly accurate here.
# filename and file_open_method are not true constants because filename is
# derived from sys.argv[1], which means it can change each time the script runs
# with different arguments. file_open_method changes based on the existence of
# save_file_path.
filename = sys.argv[1]  # pylint: disable=invalid-name
print("filename", filename)
form_fullname = FORMS_DICT[filename]
print("form_fullname", FORMS_DICT[filename])
file_open_method = "w+"  # pylint: disable=invalid-name
save_file_path = f"/var/tmp/{filename}.csv"
print("save_file_path", save_file_path)

if path.exists(save_file_path):
    os.remove(save_file_path)

for form_def in FormDef.select(lambda x: x.name == form_fullname):
    forms_data_full_list = form_def.data_class().select()
    for form_data in forms_data_full_list:
        # Check for the presente of "Paiement effectué" in form evolution
        status_to_filter_regex = re.compile("Paiement effectu.*")

        # Check if the creation_date is after 2019 and at least one name in
        # form_data.evolution matches the regular expression status_to_filter_regex

        # Retrieve creation date convertin receipt_time to datetime object
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
        #             status_to_filter_regex.match,
        #             [evolution.get_status().name for evolution in form_data.evolution],
        #         )
        #     )
        #     > 0
        # ):

        # I replaced the above commented code with the following one. It's working.
        # What follows matching_count verif in the historical code, refactored it
        if creation_date.year > 2019:
            status_names = [
                status.name
                for evolution in form_data.evolution
                if (status := evolution.get_status()) is not None
                and status.name is not None
            ]

            matching_count = sum(
                1 for _ in filter(status_to_filter_regex.match, status_names)
            )

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
                if path.exists(save_file_path):
                    file_open_method = "a"  # pylint: disable=invalid-name
                with open(
                    save_file_path, file_open_method, encoding="utf-8"
                ) as csvfile:
                    csvwriter = csv.writer(
                        csvfile,
                        delimiter="|",
                        quoting=csv.QUOTE_MINIMAL,
                        lineterminator="\n",
                    )
                    csvwriter.writerow(columns)
