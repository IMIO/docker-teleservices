# -*- coding: utf-8 -*-
# sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2
# sudo -u wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=waterloo-formulaires.guichet-citoyen.be centre_recreatif_csv.py waterloo

import csv
import re
import sys
from datetime import datetime
from time import mktime

from wcs.formdef import FormDef

lst_keeping_ids = [
    "1",
    "2",
    "90",
    "3",
    "17",
    "19",
    "18",
    "20",
    "22",
    "21",
    "23",
    "40",
    "52",
    "55",
    "56",
    "54",
    "77",
    "80",
    "151",
    "152",
    "153",
    "154",
    "155",
    "156",
    "157",
    "158",
    "159",
    "160",
    "161",
    "162",
    "163",
    "164",
    "165",
    "166",
    "167",
    "168",
    "169",
    "170",
    "171",
    "172",
    "173",
    "174",
    "175",
    "179",
    "180",
    "181",
    "182",
    "183",
    "184",
    "185",
    "186",
    "187",
    "188",
    "189",
    "190",
    "191",
    "192",
    "193",
    "194",
    "195",
    "196",
    "197",
    "198",
    "199",
    "200",
    "201",
    "202",
    "203",
    "207",
    "208",
    "209",
    "210",
    "211",
    "212",
    "213",
    "214",
    "215",
    "216",
    "217",
    "218",
    "219",
    "220",
    "221",
    "222",
    "223",
    "224",
    "225",
    "226",
    "227",
    "228",
    "229",
    "230",
    "231",
    "292",
    "293",
    "294",
    "295",
    "296",
    "297",
    "298",
    "299",
    "300",
    "301",
    "302",
    "303",
    "304",
    "305",
    "306",
    "307",
    "308",
    "309",
    "310",
    "311",
    "312",
    "313",
    "314",
    "315",
    "316",
    "264",
    "265",
    "266",
    "267",
    "268",
    "269",
    "270",
    "271",
    "272",
    "273",
    "274",
    "275",
    "276",
    "277",
    "278",
    "279",
    "280",
    "281",
    "282",
    "283",
    "284",
    "285",
    "286",
    "287",
    "288",
    "236",
    "237",
    "238",
    "239",
    "240",
    "241",
    "242",
    "243",
    "244",
    "245",
    "246",
    "247",
    "248",
    "249",
    "250",
    "251",
    "252",
    "253",
    "254",
    "255",
    "256",
    "257",
    "258",
    "259",
    "260",
    "79",
    "bo4",
    "bo2",
    "bo3",
    "bo1",
    "bo5",
    "bo6",
    "bo7",
]
intitules = []
cpt = 0

for formdef in FormDef.select(lambda x: x.id == "34", order_by="-receipt_time"):
    for formdata in formdef.data_class().select(lambda d: d.status != "draft", order_by="-receipt_time"):
        columns = []
        columns.append(formdata.get_display_id())  # identifiant du formulaire
        if formdata.receipt_time is not None:
            creation_date = datetime.fromtimestamp(mktime(formdata.receipt_time))
        columns.append(creation_date.strftime("%d/%m/%Y %H:%M:%S") or "")
        if formdata.last_update_time is not None:
            last_update_date = datetime.fromtimestamp(mktime(formdata.last_update_time))
        columns.append(last_update_date.strftime("%d/%m/%Y %H:%M:%S") or "")
        columns.append(formdata.user.get_display_name() if formdata.user else "-")
        if cpt == 0:
            intitules.append("Numéro")
            intitules.append("Date de création")
            intitules.append("Dernière modification")
            intitules.append("Nom de l'usager")
        for field in formdef.get_all_fields():  # les autres champs
            if field.id in lst_keeping_ids and field.type != "page":
                try:
                    if hasattr(field, "get_display_value"):
                        field_value = field.get_display_value(formdata.get_field_view_value(field))
                    else:
                        if field.type == "date":
                            field_value = field.get_view_value(formdata.get_field_view_value(field))
                        else:
                            field_value = formdata.get_field_view_value(field)
                    columns.append(field_value)
                    if field.id == "77":
                        # on ajoute une 2e fois pour coller a l'extract de Joel.
                        if cpt == 0:
                            intitules.append("{} - {}".format(field.label, field.id))
                        columns.append(field_value)
                    if cpt == 0:
                        intitules.append("{} - {}".format(field.label, field.id))
                except:
                    import ipdb

                    ipdb.set_trace()
        if cpt == 0:
            intitules.append("Statut")
        columns.append(formdata.get_status_label())
        if cpt == 0:
            intitules.append("Anonymisé")
        if formdata.anonymised is None:
            columns.append("Non")
        else:
            columns.append("Oui")

        with open("/var/tmp/{}.csv".format(sys.argv[1]), "a") as csvfile:
            csvwriter = csv.writer(csvfile, delimiter="|", quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
            if cpt == 0:
                csvwriter.writerow(intitules)
            csvwriter.writerow(columns)
        cpt = cpt + 1
